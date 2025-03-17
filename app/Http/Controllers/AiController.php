<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\Process\Process as SymfonyProcess;
use Illuminate\Support\Str;

class AiController extends Controller
{
    // public function generate(Request $request)
    // {
    //     $prompt = $request->input('prompt');

    //     $pythonScript = str_replace('/', '\\', base_path('SQLDrama/prompt.py'));
    //     $cmd = "python \"$pythonScript\" " . escapeshellarg($prompt);
    //     $output = shell_exec($cmd . " 2>&1");

    //     $response = json_decode($output, true);

    //     // dd($response["sql"]);

    //     return response()->stream(function () use ($response) {
    //         echo "event: message\n";
    //         echo "data: " . json_encode(['status' => 'story', 'text' => $response['story']]) . "\n\n";
    //         ob_flush();
    //         flush();

    //         // After typing ends, send SQL query
    //         sleep(2); // small pause for effect
    //         echo "event: message\n";
    //         echo "data: " . json_encode(['status' => 'sql', 'query' => $response['sql']]) . "\n\n";

    //         ob_flush();
    //         flush();
    //     }, 200, [
    //         "Content-Type" => "text/event-stream",
    //         "Cache-Control" => "no-cache",
    //         "Connection" => "keep-alive",
    //     ]);
    // }

    public function generate(Request $request) {
        $hasMapping = false;
        $bufferData = null;
        // Validate the request
        $request->validate([
            'prompt' => 'required|string',
            'model' => 'nullable|string',
            'export' => 'nullable|string'
        ]);

        // Get the prompt from the request
        $prompt = $request->input('prompt');
        $model = $request->input('model', 'gemini');
        $export = $request->input('export', 'csv');
        $export_path = base_path('storage\temp');

        $cacheKey = 'ai_response_' . md5($prompt);

        if (Cache::has($cacheKey)) {
            $cachedResponse = Cache::get($cacheKey);

            // Stream the cached response
            return response()->stream(function () use ($cachedResponse) {
                echo $this->formatChunk([
                    'type' => 'story',
                    'content' => 'Fetching response from cache...'
                ]);
                flush();

                // Stream cached data
                // foreach ($cachedResponse as $chunk) {
                //     echo $this->formatChunk($chunk);
                //     flush();
                // }

                $data = json_decode($cachedResponse, true);
                if (json_last_error() === JSON_ERROR_NONE) {
                    echo $this->formatChunk($data);
                    flush();
                }

                // Send completion message
                echo $this->formatChunk([
                    'type' => 'completion',
                    'content' => 'Process completed (from cache)'
                ]);
            }, 200, [
                'Cache-Control' => 'no-cache',
                'Content-Type' => 'text/event-stream',
                'X-Accel-Buffering' => 'no'
            ]);
        }

        // Process the request in a separate thread to allow streaming
        return response()->stream(function () use ($prompt, $model, $export, $export_path, $cacheKey) {
            // Call Python script to generate the query
            $pythonProcess = new SymfonyProcess([
                'python',
                base_path('SQLDrama/prompt.py'),
                trim($prompt, "'"),
                trim($model, "'"),
                trim($export, "'"),
                trim($export_path, "'")
            ]);
            $pythonProcess->setTimeout(120); // 2 minutes timeout
            $pythonProcess->start();

            // First, send status that script is starting
            echo $this->formatChunk([
                'type' => 'start',
                'content' => 'Starting to analyze your request...'
            ]);
            flush();

            // Wait for the process to finish
            $pythonProcess->wait(function ($type, $buffer) use ($cacheKey) {
                if ($type === SymfonyProcess::OUT) {
                    try {
                        Cache::put($cacheKey, $buffer, 10 * 60);
                        $data = json_decode($buffer, true);
                        if (json_last_error() === JSON_ERROR_NONE) {
                            echo $this->formatChunk($data);
                            flush();
                        }
                    } catch (\Exception $e) {
                        // Just log the error, don't send to client
                        Log::error('Error parsing Python output: ' . $e->getMessage());
                    }
                } else if ($type === SymfonyProcess::ERR) {
                    // This handles the error output from the process
                    Log::error('Python script error: ' . $buffer);
                    echo $this->formatChunk([
                        'type' => 'error',
                        'content' => 'Error executing Python script: ' . $buffer
                    ]);
                    flush();
                }
            });

            // Send completion message
            echo $this->formatChunk([
                'type' => 'completion',
                'content' => 'Process completed'
            ]);

        }, 200, [
            'Cache-Control' => 'no-cache',
            'Content-Type' => 'text/event-stream',
            'X-Accel-Buffering' => 'no'
        ]);
    }

    public function download($filename)
    {
        $path = storage_path('temp/' . $filename);
        if (!file_exists($path)) {
            abort(404);
        }
        return response()->download($path);
    }

    /**
     * Format chunk for SSE streaming
     */
    private function formatChunk($data)
    {
        return 'data: ' . json_encode($data) . "\n\n";
    }
}
