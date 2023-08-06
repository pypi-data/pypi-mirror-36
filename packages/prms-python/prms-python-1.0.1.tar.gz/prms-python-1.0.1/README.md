# PRMS-Python

PRMS-Python provides a Python interface to PRMS data files and manages 
PRMS simulations. This module aims to improve the efficiency of PRMS 
workflows by giving access to PRMS data structures while providing 
"pythonic" tools to do scenario-based PRMS simulations. By 
"scenario-based" we mean testing model hypotheses associated with model 
inputs, outputs, and model structure. For example, parameter sensitivity 
analysis, where each "scenario" is an iterative perturbation of one or 
many parameters. Another example "scenario-based" modeling exercise 
would be climate scenario modeling: what will happen to modeled outputs 
if the input meteorological data were to change?



## Installation

PRMS-Python versions are available on the Python Package Index [PyPI](https://pypi.org/project/prms-python/)
and can be installed and upgraded using pip:

```
pip install prms-python
```

Alternatively clone-then-pip:

```
git clone https://github.com/PRMS-Python/PRMS-Python.git
cd PRMS-Python
```

then

```
pip install --editable .
```

Another option is to download the source code as a zip file, unzip it
and within the PRMS-Python root directory run:

```
python setup.py install
```

## Usage and documentation

We reccomend starting with the ["getting started"](https://github.com/PRMS-Python/PRMS-Python/blob/master/notebooks/getting_started.ipynb) 
Jupyter notebook for file structure rules that PRMS-Python uses and then
moving on to other example notebooks in the [`notebooks` directory](https://github.com/PRMS-Python/PRMS-Python/tree/master/notebooks). Online documentation is available [here](https://prms-python.github.io/PRMS-Python/build/html/index.html).

## Building documentation

This project uses the [Sphinx documentation engine for Python](http://www.sphinx-doc.org/en/master/)
The documentation source is located in `docs/source`. Eventually we can
wrap the following steps into a script. But for now, to build the
documentation, go to the `docs/` directory and run

```
make html
```

If it fails because of missing dependencies, just install the dependencies 
it says it's missing. Publishing the docs is now done automatically with any 
commits are pushed to the master branch.


<!---  commented the published of online docs the old way
  The method I employed was found on the Sphinx repository as an issue
  that did exactly what I wanted: https://github.com/sphinx-doc/sphinx/issues/3382
  essentially using the new github publish docs from master branch doc folder
  but using a fake index.html to redirect github to the one under docs/build/html/

If it succeds and this is your first time making the html docs you will see a 
new directory, `build/html`. If this is the first time you've 
built and updated the documentation you'll need to run this first

```
git remote add docs http://github.com/PRMS-Python/docs
```

Now, we'll create a branch that consists solely 
of this built html by running the following command from the root of the 
PRMS-Python documentation directory

```
git checkout -b new-docs \
    && git add -f docs/build/html \
    && git commit -m"built updated docs" \
    && git filter-branch -f --prune-empty --subdirectory-filter docs/build/html new-docs \
    && git push -u docs HEAD:new-docs
```

This pushed the newly built documentation to the `PRMS-Python/docs` repository.
Now we just have to move the new branch you pushed to GitHub to be the
`gh-pages` branch.

First, change directories to the PRMS-Python/docs repository. Then,

```
git fetch origin \
    && git checkout new-docs \
    && git push --delete gh-pages \
    && git push -u origin HEAD:gh-pages \
    && git push --delete origin new-docs \
    && git branch -D new-docs
```

-->


## Unit tests

I run them using nose but that's not required. From the root repo directory

```
nosetests -v
```

## Contribute

We welcome anyone seriously interested in contributing to PRMS-Python to do so in anyway they see fit. If you are not sure where to begin you can look for current issues or submit a new issue [here](https://github.com/PRMS-Python/PRMS-Python/issues). You may also [fork](https://help.github.com/articles/fork-a-repo/) PRMS-Python and submit a pull request if you would like to offer your direct changes to the package. 

<!---  commented until paper accepted

## Citing PRMS-Python

If you use PRMS-Python for published work we ask that you cite it as follows:

-->
