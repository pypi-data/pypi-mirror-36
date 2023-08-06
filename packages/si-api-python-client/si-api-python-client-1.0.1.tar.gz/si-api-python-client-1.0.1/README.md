# contribute
```
# https://github.com/pypa/pipenv
pipenv install -e .
pipenv shell

SI_API_KEY={apikey} pipenv run python main.py {image}


# install new package
pipenv install requests


```

# DEPLOY
```
pipenv install -e .
pipenv run python setup.py sdist
pipenv run twine check dist/*
pipenv run twine upload dist/*
```