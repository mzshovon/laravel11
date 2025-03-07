<?php

use App\Http\Controllers\AiController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

Route::post('/send-prompt', [AiController::class, 'generate']);
Route::get('/generate', [AiController::class, 'generate']);
Route::get('/download/{filename}', [AiController::class, 'download']);
