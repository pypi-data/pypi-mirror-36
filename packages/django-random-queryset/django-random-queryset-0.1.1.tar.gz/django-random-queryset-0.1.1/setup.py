from setuptools import setup


setup(
    name='django-random-queryset',
    version='0.1.1',
    author='Roman M. Remizov',
    author_email='rremizov@yandex.ru',

    license='MIT',
    platforms=['any'],
    description="The extension gives you ability to pull random records using Django's ORM.",
    long_description=open('README.rst').read(),
    url='http://github.com/rremizov/django-random-queryset',

    packages=[
        'django_random_queryset',
    ],
    install_requires=[
        'django>=1.7',
    ],

    test_suite='tests.run_tests.run_all',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
