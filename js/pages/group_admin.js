app.endpoint_handler('group', function() {

    $('form.git-group-delete').each(function() {
        var $form = $(this);
        var name = $form.data('group-name');
        var prompt = "DELETE " + name;
        $form.formIsDangerous({
            message: 'This can <strong>NOT</strong> be undone.<br/>If you are sure, type <code>' + prompt + '</code>.',
            prompt: prompt,
        });
    });

});
