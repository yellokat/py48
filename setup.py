from setuptools import setup, find_packages

setup(
    name                = 'py48',
    version             = '0.8',
    description         = 'Korean fortune telling package using birthdate and time',
    author              = 'yellokat',
    author_email        = 'jenova195@gmail.com',
    url                 = 'https://github.com/yellokat/py48',
    download_url        = 'https://github.com/jeakwon/ccpy/archive/0.0.tar.gz',
    install_requires    =  ['pandas'],
    packages            = find_packages(exclude = []),
    keywords            = [],
    python_requires     = '>=3',
    package_data        = {'py48' : ['절입데이터.csv']},
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)