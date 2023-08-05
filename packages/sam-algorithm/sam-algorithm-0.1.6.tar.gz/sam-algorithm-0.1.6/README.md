# self-assembling-manifold
The Self-Assembling-Manifold (SAM) algorithm.

# Installation:
SAM runs using python3.6 and has not yet been tested for backwards compatibility. Python can be installed using Anaconda.

Download Anacodna from here:
    https://www.anaconda.com/download/

Create and activate a new environment with python3.6 as follows:
```
conda create -n environment_name python=3.6
conda activate environment_name
```

Having activated the environment, SAM can be downloaded from the PyPI repository using pip or, for the development version, downloaded from the github directly.

PIP install:
```
pip install sam-algorithm
```

Development version install:
```
git clone https://github.com/atarashansky/self-assembling-manifold.git
cd self-assembling-manifold
python setup.py install
```

# Usage:
Please see the Jupyter notebook in the 'tutorial' folder for a basic tutorial. If you installed a fresh environment, do not forget to install jupyter into that environment! Please run
```
pip install jupyter
```
in your conda environment.

# Citation:
If using the SAM algorithm, please cite the following preprint:
https://www.biorxiv.org/content/early/2018/07/07/364166

# Adding extra functionality:
In its current form, this is just a lightweight implementation of the SAM algorithm. If there is any added functionality you would like to see added for downstream analysis, such as cell clustering, differential gene expression analysis, data exporting, etc, please let me know by submitting a new issue describing your request and I will do my best to add that feature.
