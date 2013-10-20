import os


def setup_config(app):

    our_path = os.path.abspath(os.path.join(__file__, '..', '..'))

    root_path = os.environ.get('FLASK_ROOT_PATH')
    if not root_path:
        package_name = app.name.split('.')[0]
        package = __import__(package_name)
        root_path = os.path.abspath(os.path.join(package.__file__, '..', '..'))

    instance_path = os.environ.get('FLASK_INSTANCE_PATH')
    if not instance_path:
        instance_path = os.path.join(root_path, 'var')

    # Scan $root/etc/flask for config files. They are included
    # in sorted order, without respect for the base of their path.
    config_files = set()
    for root in (our_path, root_path, instance_path):
        dir_path = os.path.join(root, 'etc', 'flask')
        if not os.path.exists(dir_path):
            continue
        for file_name in os.listdir(dir_path):
            if os.path.splitext(file_name)[1] == '.py':
                config_files.add(os.path.join(dir_path, file_name))

    config_files = sorted(config_files, key=lambda path: os.path.basename(path))

    basics = dict(
        ROOT_PATH=root_path,
        INSTANCE_PATH=instance_path,
    )
    namespace = {}
    basics['setdefault'] = namespace.setdefault
    for path in config_files:
        namespace.update(basics)
        execfile(path, namespace)

    app.config.update(namespace)
    app.config.update(basics)
    app.root_path = root_path
    app.instance_path = instance_path
