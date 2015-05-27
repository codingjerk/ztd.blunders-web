(function() {
    function onResultAprooved(data) {
        console.log(data)

        if (data.status !== 'ok') {
            // TODO: Show notify
            return;
        }

        window.location.href = '/'
    }

    $('#submit').on('click', function() {
        $.ajax({
            type: 'POST',
            url: "/signup",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $('#username').val(),
                password: $('#password').val(),
                email:    $('#email').val(),
            })
        }).done(onResultAprooved);
    });
})();