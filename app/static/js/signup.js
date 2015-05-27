(function() {
    function onResultAprooved(data) {
        // @TODO
    }

    $('#submit').on('click', function() {
        console.log($('#username').val())
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