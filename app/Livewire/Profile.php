<?php

namespace App\Livewire;

use App\Models\User;
use Livewire\Component;
use Livewire\WithPagination;

class Profile extends Component
{
    use WithPagination;

    public string $userName;
    public int $perPage = 10;
    public string $search = "";
    public string $sortingDirection = "ASC";
    public string $sortingColumn = "name";

    public string $userProfileImage;

    public function mount()
    {
        $this->userName = auth()->user()->name ?? "dummy";
        $this->userProfileImage = auth()->user()->image ?? "https://www.pngall.com/wp-content/uploads/5/User-Profile-PNG-Image.png";
    }

    public function sort($column)
    {
        if($this->sortingColumn === $column) {
            $this->sortingDirection = ($this->sortingDirection === "ASC") ? "DESC" : "ASC";
            return;
        }
        $this->sortingColumn = $column;
        $this->sortingDirection = "ASC";
    }

    public function updatedPerPage()
    {
        $this->resetPage();
    }

    public function updatedSearch()
    {
        $this->resetPage();
    }

    public function render()
    {
        return view('livewire.profile', [
            'users' => User::search($this->search)
                        ->orderBy($this->sortingColumn, $this->sortingDirection)
                        ->paginate($this->perPage)
        ]);
    }
}
