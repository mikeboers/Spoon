from distutils.core import setup

setup(
    name='spoon',
    version='0.0.1',
    description='Lightweight personal git server.',
    url='http://github.com/mikeboers/spoon',
    
    packages=['spoon'],
    
    author='Mike Boers',
    author_email='spoon@mikeboers.com',
    license='BSD-3',
    
    entry_points={
        'console_scripts': [
            'spoon-shell = spoon.commands.shell:main',
            'spoon-import = spoon.commands.import:main',
            'spoon-account = spoon.commands.account:main',
            'spoon-keys = spoon.commands.keys:main',
        ],
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
    ],
    
)
