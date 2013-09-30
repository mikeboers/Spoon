app.endpoint_handler('cpanel_users', function() {

    $('.btn[data-action="auth.token.create"]').each(function() {
        var $this = $(this);
        $this.click(function() {
            vex.open({
                content: '<input type="text" value="blah blah blah" />'
            });
        })
    });
})
