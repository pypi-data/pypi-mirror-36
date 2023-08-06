import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as readme:
    README = readme.read()

setup(
    name='django-localized-fields',
    version='5.0a4',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    license='MIT License',
    description='Implementation of localized model fields using PostgreSQL HStore fields.',
    long_description=README,
    url='https://github.com/SectorLabs/django-localized-fields',
    author='Sector Labs',
    author_email='open-source@sectorlabs.ro',
    keywords=['django', 'localized', 'language', 'models', 'fields'],
    install_requires=[
        'django-postgres-extra>=1.21a11',
        'Django>=1.11',
        'deprecation==2.0.3'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
