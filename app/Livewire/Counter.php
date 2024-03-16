<?php

namespace App\Livewire;

use Livewire\Component;

class Counter extends Component
{
    public int $count = 0;

    public function increment()
    {
        return $this->count++;
    }

    public function decrement()
    {
        return $this->count > 0 && $this->count--;
    }

    public function render()
    {
        return view('livewire.counter');
    }
}
