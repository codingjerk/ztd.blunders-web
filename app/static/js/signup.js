(function() {
    function onResultAprooved(data) {
        if (data.status !== 'ok') {
            notify.error(data.message);
            return;
        }

        location.replace('/training');
    }

    $('#submit').on('click', function() {
        $.ajax({
            type: 'POST',
            url: "/signup",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $('#username').val(),
                password: $('#password').val(),
                email:    $('#email').val()
            })
        }).done(onResultAprooved);
    });
})();