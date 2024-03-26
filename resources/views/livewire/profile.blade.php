<div>
    <div class="mb-3">
        <x-text-input wire:model.live.debounce.200ms='search' id="search" class="block mt-1"
                        type="text"
                        name="search"
                        placeholder="Search...." />

        <x-input-error :messages="$errors->get('password')" class="mt-2" />
    </div>
    <table class="table table-striped">
        <thead>
            <tr style="cursor: pointer">
                <th scope="col" wire:click='sort("id")'>#</th>
                <th scope="col" wire:click='sort("name")'>Name</th>
                <th scope="col"  wire:click='sort("email")'>Email</th>
                <th scope="col" wire:click='sort("created_at")'>Created At</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($users as $user)
            <tr wire:key="{{ $user['id'] }}">
                <th scope="row">{{ $user['id'] }}</th>
                <td>{{ $user['name'] }}</td>
                <td>{{ $user['email'] }}</td>
                <td>{{ \Carbon\Carbon::parse($user['created_at'])->format("h:i a, d-m-Y") }}</td>
            </tr>
            @endforeach

        </tbody>
    </table>
    <div class="py-2 px-2">
        <div class="flex">
            <div class="flex space-x-2 items-center mb-2">
                <label class="me-2">Per page</label>
                <select wire:model.live="perPage">
                    <option value="10">10</option>
                    <option value="20">20</option>
                    <option value="50">50</option>
                </select>
            </div>
        </div>
    </div>
    {{$users->links(data: ['scrollTo' => false])}}
</div>
