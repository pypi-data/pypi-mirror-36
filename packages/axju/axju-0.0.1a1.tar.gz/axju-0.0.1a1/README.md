# axju
comming soon.

## Install
```bash
pip install axju
```

## development
Clone repo:
```bash
git clone https://github.com/axju/axju.git
```
Create virtual environment and update dev-tools:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade wheel pip setuptools twine
```
Install wpexport:
```bash
pip install -e .
```
Publish the packages:
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```
