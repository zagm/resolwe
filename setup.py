import os.path
import setuptools

# Get the long description from README.
with open('README.rst', 'r') as fh:
    long_description = fh.read()

# Get package metadata from '__about__.py' file.
about = {}
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, 'resolwe', '__about__.py'), 'r') as fh:
    exec(fh.read(), about)

setuptools.setup(
    name=about['__title__'],
    use_scm_version=True,
    description=about['__summary__'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__url__'],
    license=about['__license__'],
    # Exclude tests from built/installed package.
    packages=setuptools.find_packages(
        exclude=['tests', 'tests.*', '*.tests', '*.tests.*']
    ),
    package_data={
        'resolwe': [
            'flow/executors/requirements.txt',
            'flow/static/flow/*.json',
            'toolkit/processes/**.yml',
            'toolkit/tools/**.py',
        ]
    },
    python_requires='>=3.6, <3.8',
    install_requires=[
        'asteval~=0.9.12',
        'async-timeout~=3.0.0',
        'channels~=2.2.0',
        'channels_redis~=2.4.0',
        'Django~=2.2.0',
        'djangorestframework~=3.9.0',
        'django-filter~=2.0.0',
        'django-guardian~=1.5.0',
        'django-versionfield2~=0.5.0',
        'django-fernet-fields~=0.5',
        'django-priority-batch~=2.0.0',
        'elasticsearch-dsl~=6.3.1',
        'Jinja2~=2.10.1',
        'jsonschema~=2.6.0',
        'plumbum~=1.6.6',
        'psycopg2-binary~=2.8.0',
        'PyYAML~=5.1',
        'redis~=3.2.0',
        'resolwe-runtime-utils~=2.0.1',
        'shellescape~=3.4.1',
        'Sphinx>=1.5.1, <1.7.0',
        # XXX: Temporarily pin urllib to 1.24.x, since requests 2.21.0
        # has requirement urllib3<1.25,>=1.21.1
        'urllib3~=1.24.2',
        'wrapt~=1.11.1',
   ],
    extras_require={
        'docs': ['sphinx_rtd_theme'],
        'package': ['twine', 'wheel'],
        'test': [
            'check-manifest',
            'coverage>=4.2',
            'pycodestyle~=2.5.0',
            'pydocstyle~=3.0.0',
            'pylint~=2.3.1',
            'readme_renderer',
            'setuptools_scm',
            'testfixtures>=4.10.0',
            'tblib>=1.3.0',
            'isort~=4.3.12',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='resolwe dataflow django',
)
