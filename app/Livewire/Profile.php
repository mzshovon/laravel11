<?php

namespace App\Livewire;

use App\Models\User;
use Livewire\Component;
use Livewire\WithPagination;

class Profile extends Component
{
    use WithPagination;
    public string $userName;

    public string $userProfileImage;

    public function mount()
    {
        $this->userName = auth()->user()->name ?? "dummy";
        $this->userProfileImage = auth()->user()->image ?? "https://www.pngall.com/wp-content/uploads/5/User-Profile-PNG-Image.png";
    }

    public function render()
    {
        return view('livewire.profile', [
            'users' => User::paginate(10)
        ]);
    }
}
