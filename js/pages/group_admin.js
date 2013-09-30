app.endpoint_handler('group', function() {

    $('.git-group-delete-btn').each(function() {
        var $this = $(this);
        console.log(this);
        $this.click(function(e) {
            e.preventDefault();
            vex.dialog.confirm({
                message: 'Are you sure? This cannot be undone!',
                callback: function(res) {
                    if (res) {
                        $this.closest('form').submit();
                    }
                }
            });
        });
    });

});
