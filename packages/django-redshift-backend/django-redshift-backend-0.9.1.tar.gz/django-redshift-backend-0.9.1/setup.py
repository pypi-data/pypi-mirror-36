from setuptools import setup, find_packages
import os

requires = [
    'django',
    'psycopg2',
]


def read(filename):
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(fpath) as f:
        return f.read()


setup(
    name='django-redshift-backend',
    version='0.9.1',
    packages=find_packages(),
    url='https://github.com/shimizukawa/django-redshift-backend',
    license='Apache Software License',
    author='shimizukawa',
    author_email='shimizukawa@gmail.com',
    description='Redshift database backend for Django',
    long_description=read('README.rst') + read('CHANGES.rst'),
    install_requires=requires,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
