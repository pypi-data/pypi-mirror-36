"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'marshmallow>=2.15.0,<3.0',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='marshmallowjson',
    version='0.4.3',
    description="Turns a JSON type definition into a marshmallow validation and serialization toolkit.",
    long_description=readme + '\n\n' + history,
    author="Oscar David Arbeláez",
    author_email='odarbelaeze@gmail.com',
    url='https://github.com/tech-teach/marshmallowjson',
    packages=find_packages(include=['marshmallowjson']),
    entry_points={
        'console_scripts': [
            'marshmallowjson=marshmallowjson.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='marshmallowjson',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
