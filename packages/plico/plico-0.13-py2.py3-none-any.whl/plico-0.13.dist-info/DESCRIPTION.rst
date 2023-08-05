# PLICO: Python Laboratory Instrumentation COntrol

This is just a framework for a typical HW controlling application

## Installation

### Installing
From the wheel
```
pip install plico-XXX.whl
```

In plico source dir
```
pip install .
```

During development you want to update use

```
pip install -e .
```
that install a python egg with symlinks to the source directory in such 
a way that chages in the python code are immediately available without 
the need for re-installing (beware of conf/calib files!)

### Uninstall

```
pip uninstall plico
```




## Administration Tool

For developers.


### Testing
Never commit before tests are OK!
To run the unittest and integration test suite execute in plico source dir

```
python setup.py test
```


### Creating a Conda environment
Use the Anaconda GUI or in terminal

```
conda create --name plico 
```

To create an environment with a specific python version

```
conda create --name plico26  python=2.6
```


It is better to install available packages from conda instead of pip. 

```
conda install --name plico matplotlib scipy ipython numpy
```

### Packaging and distributing

See https://packaging.python.org/tutorials/distributing-packages/#

To make a source distribution

```
python setup.py sdist
```

and the tar.gz is created in plico/dist


If it is pure Python and works on 2 and 3 you can make a universal wheel 

```
python setup.py bdist_wheel --universal
```

Otherwise do a pure wheel

```
python setup.py bdist_wheel
```

The wheels are created in plico/dist. I suppose one can trash plico/build now and distribute the files in plico/dist


To upload on pip (but do you really want to make it public?)

```
twine upload dist/*
```

