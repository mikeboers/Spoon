import os


def make_config(app):

    our_path = os.path.abspath(os.path.join(__file__, '..', '..'))

    package_name = app.name.split('.')[0]
    package = __import__(package_name)
    root_path = os.path.abspath(os.path.join(package.__file__, '..', '..'))
    instance_path = os.path.join(root_path, 'var')

    # Scan etc/flask and var/etc/flask for config files. They are included
    # in sorted order, without respect for if they are in "var/" or not.
    config_files = []
    for root in (our_path, root_path, instance_path):
        dir_path = os.path.join(root, 'etc', 'flask')
        print dir_path
        if not os.path.exists(dir_path):
            continue
        for file_name in os.listdir(dir_path):
            if os.path.splitext(file_name)[1] == '.py':
                config_files.append(os.path.join(dir_path, file_name))
    config_files.sort(key=lambda path: os.path.basename(path))

    basics = dict(
        ROOT_PATH=root_path,
        INSTANCE_PATH=instance_path,
    )
    namespace = dict(basics)
    for path in config_files:
        namespace.update(basics)
        execfile(path, namespace)

    return namespace
