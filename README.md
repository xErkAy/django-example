# An example of structure for Django application


## Project uses:
* Ruff - a Python linter
* Mypy - a static type checker for Python
```
make check - check your project
make fmt - format your project
make lint - check & format your project
```


###
## How to run a project
```
git clone ...
cd django-example
```

```
pip install -r requirements.txt
```

```
python src/manage.py migrate
python src/manage.py runserver
```


###
## Available paths
```
/api/auth/
/api/registration/

/api/upload/
/api/download/
/api/test/
```


