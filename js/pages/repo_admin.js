app.endpoint_handler('repo_admin', function() {
    
    $('form.git-repo-delete').each(function() {
        var $form = $(this);
        var name = $form.data('repo-name');
        var prompt = "DELETE " + name;
        $form.formIsDangerous({
            message: 'This can <strong>NOT</strong> be undone.<br/>If you are sure, type <code>' + prompt + '</code>.',
            prompt: prompt,
        });
    });

});
