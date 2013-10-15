import os

# Scan etc/flask and var/etc/flask for config files. They are included
# in sorted order, without respect for if they are in "var/" or not.
ROOT_PATH = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
config_files = []
for dir_name in 'etc/flask', 'var/etc/flask':
    dir_path = os.path.join(ROOT_PATH, dir_name)
    if not os.path.exists(dir_path):
        continue
    for file_name in os.listdir(dir_path):
        if os.path.splitext(file_name)[1] == '.py':
            config_files.append(os.path.join(dir_path, file_name))
config_files.sort(key=lambda path: os.path.basename(path))

for path in config_files:
    execfile(path)
