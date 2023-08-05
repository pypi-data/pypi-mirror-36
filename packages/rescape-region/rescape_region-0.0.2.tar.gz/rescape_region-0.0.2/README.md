=====
Rescape-Region
=====

A Django app to support limiting users by geographic region

Quick start
-----------

1. Add "region-app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'regional',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('regional/', include('regional.urls')),

3. Run `python manage.py migrate` to create the regional models.

## Installation

Create a virtual environment using
```bash
mkdir ~/.virtualenvs
python3 -m venv ~/.virtualenvs/rescape-region
Activate it
source ~/.virtualenvs/rescape-region/bin/activate
```

#### Install requirements
```bash
$VIRTUAL_ENV/bin/pip install --no-cache-dir  --upgrade -r requirements.txt
```

Add the following to the bottom $VIRTUAL_ENV/bin/activate to setup the PYTHONPATH.
Replace the path with your code directory

```bash
export RESCAPE_REGION_BASE_DIR=/Users/andy/code/rescape-graphene
export RESCAPE_REGION_PROJECT_DIR=$RESCAPE_REGION_BASE_DIR/urbinsight
export PYTHONPATH=.:$RESCAPE_REGION_BASE_DIR:$RESCAPE_REGION_PROJECT_DIR
```

## Build

Update the version in setup.py
Run to generate build:
Update the version with bumpversion, which can't seem to look it up itself but updates setup.py

```bash
git commit . -m "Version update" && git push
bumpversion --current-version {look in setup.py} patch setup.py
python3 setup.py clean sdist bdist_wheel
```

To distribute to pypi site:
Upload package:

```bash
twine upload dist/*
```

All at once:
```bash
git commit . -m "Version update" && git push && bumpversion --current-version {look in setup.py} patch setup.py && python3 setup.py clean sdist bdist_wheel && twine upload dist/*
```

For setup of testpypi see ~/.pypirc or create one according to the testpypi docs:
e.g.:
[distutils]
index-servers=
    pypi
    testpypi

[testpypi]
repository: https://test.pypi.org/legacy/
username: your username for pypi.org
