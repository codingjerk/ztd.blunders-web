(function() {
    $('#submit').on('click', signup);
    $('#validate').on('click', validate);

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
                email:    $('#email').val(),
                validation_code: $('#validation_code').val(),
            },
            onDone: onResultAprooved
        });
    }

    function validate() {
        sync.ajax({
            id: 'validate',
            url: '/api/session/validate',
            data: {
                username: $('#username').val(),
                password: $('#password').val(),
                email:    $('#email').val()
            },
            onDone: onValidationSent
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

    function onValidationSent(data) {
        if (data.status !== 'ok') {
            if (data.field) {
                notify.inplaceError(data.field, data.message);
            } else {
                notify.error(data.message);
            }

            return;
        }
    }

})();
