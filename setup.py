from setuptools import setup

setup(
    name='plzrebase',
    version='0.1.0',
    url='https://github.com/kiwicom/plzrebase',
    author='Simone Esposito',
    author_email='simone@kiwi.com',
    download_url='https://github.com/kiwicom/plzrebase',
    description='GitLab CI + Force people to rebase',
    packages=['plzrebase'],
    entry_points={'console_scripts': 'plzrebase=plzrebase:main'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
