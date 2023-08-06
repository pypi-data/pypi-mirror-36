# unapid
Prints some useful tables.

## Install:

<!-- Test newly uploaded distribution: -->
python -m pip install unapid

## Example use:

python -m unapid

## Packaging:

I'm using the following tutorial to upload my project to git so that it can be installed via pip:
https://packaging.python.org/tutorials/packaging-projects/#create-an-account

<!--
  1) Create project from git because it automatically creates:
       - README.md
       - LICENSE
  2) Create a __init__.py file inside project/project directory
  3) Create a setup.py file in project directory (copy from above website)
 -->

<!-- Install/upgrade setuptools/wheel (not every time)-->
<!-- python -m pip install --user --upgrade setuptools wheel -->

<!-- Install/update twine (not every time) -->
<!-- python3 -m pip install --user --upgrade twine -->

<!-- Generate distribution: -->
python setup.py sdist bdist_wheel

<!-- Upload distribution: -->
twine upload dist/*
