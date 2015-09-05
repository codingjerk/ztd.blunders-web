(function() {
    $('#submit').on('click', signup);

    $(document).keyup(function(event) {
        if (event.keyCode === 13) {
            signup();
        }
    });

    function signup() {
        sync.ajax({
            id: 'submit',
            url: '/api/session/signup',
            data: {
                username: $('#username').val(),
                password: $('#password').val(),
                email:    $('#email').val()
            },
            onDone: onResultAprooved
        });
    }

    function onResultAprooved(data) {
        if (data.status !== 'ok') {
            if (data.field) {
                notify.inplaceError(data.field, data.message);
            } else {
                notify.error(data.message);
            }             
            
            return;
        }

        location.replace('/training');
    }
})();