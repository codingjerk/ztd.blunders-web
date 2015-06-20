(function setupListeners() {
    $('#logout-button').on('click', function () {
        $.ajax({
            type: 'POST',
            url: "/logout",
            contentType: 'application/json'
        }).done(function(data) {
            if (data.status !== 'ok') {
                notify.error(data.message);               
                return;
            }

            location.reload();
        });
    });
})();