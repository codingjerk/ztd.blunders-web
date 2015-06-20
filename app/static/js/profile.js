(function updateProfile() {
    function onUpdateProfileRequest(response) {
        if (response.status !== 'ok') {
            notify.error(response.message);
            return;
        }

        grid.update(response.data);
    }

    $.ajax({
        type: 'POST',
        url: "/getUserProfile",
        contentType: 'application/json',
        data: JSON.stringify({
            username: $.url('?user')
        })
    }).done(onUpdateProfileRequest);
})();
