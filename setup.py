from distutils.core import setup

setup(
    name='gitbase',
    version='0.0.1',
    description='Lightweight personal git server.',
    url='http://github.com/mikeboers/git-base',
    
    packages=['gitbase'],
    
    author='Mike Boers',
    author_email='git-base@mikeboers.com',
    license='BSD-3',
    
    entry_points={
        'console_scripts': [
            'git-base-shell = gitbase.shell:main',
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
