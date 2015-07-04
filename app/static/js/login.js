(function setupListeners() {
    $('#login-button').on('click', login);
    
    $(document).keyup(function(event) {
        if (event.keyCode === 13) {
            login();
        }
    });

    function login() {
        sync.ajax({
            id: 'login-button',
            url: '/login',
            data: {
                username: $('#username').val(),
                password: $('#password').val()
            },
            onDone: function(data) {
                if (data.status !== 'ok') {
                    if (data.field) {
                        notify.inplaceError(data.field, data.message);
                    } else {
                        notify.error(data.message);
                    }             
                    
                    return;
                }

                location.replace(document.referrer);
            }
        });
    }
})();