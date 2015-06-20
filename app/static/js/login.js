(function setupListeners() {
    $('#login-button').on('click', function () {
        $.ajax({
            type: 'POST',
            url: "/login",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $('#username').val(),
                password: $('#password').val()
            })
        }).done(function(data) {
            if (data.status !== 'ok') {
                if (data.field) {
                    notify.inplaceError(data.field, data.message);
                } else {
                    notify.error(data.message);
                }             
                
                return;
            }

            location.replace(document.referrer);
        });
    });
})();