<div>
    <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Email</th>
            <th scope="col">Created At</th>
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
      {{$users->links(data: ['scrollTo' => false])}}
</div>
