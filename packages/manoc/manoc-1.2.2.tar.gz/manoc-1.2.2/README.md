### Build

```
virtualenv -p python3 venv
. venv/bin/activate
pip install --editable .

...

deactivate
```

### Distr

```
python3 setup.py sdist bdist_wheel
twine upload dist/*
```


### Docker Build
```
docker build -t sekolq/manoc:1.0 .
docker build -t artifactorycn.netcracker.com:17009/seko0313/manoc:1.0 .
docker push sekolq/manoc:1.0
docker push artifactorycn.netcracker.com:17009/seko0313/manoc:1.0
```

### Code completion
```
eval "$(_MANOC_COMPLETE=source manoc)"
```

### Use

```

```