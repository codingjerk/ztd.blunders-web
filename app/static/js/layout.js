(function setupListeners() {
    $('#logout-button').on('click', function () {
        $.ajax({
            type: 'POST',
            url: "/logout",
            contentType: 'application/json'
        }).done(function(data) {
            if (data.status !== 'ok') {
                console.log('Unable to logout!');// TODO: notify                
                return;
            }

            location.reload();
        });
    });
})();