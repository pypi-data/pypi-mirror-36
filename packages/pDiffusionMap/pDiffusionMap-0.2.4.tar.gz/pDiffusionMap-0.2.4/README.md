# DiffusionMap

## Introduction
This package is created to conduct diffusion map with
python and mpi in a user friendly way. This project 
is written in python with almost standard python package dependence. 

Currently this package can handle input from hdf5 files.

## Usage
This package is developed to use at SLAC and some other supercomputers. Since this is 
only at a starting stage, I will only write down the usage of this package at the SLAC 
psana server.

In the diffusion map algorithm, one first calculate the pairwise similarity matrix, and 
then construct the normalized symmetric Laplacian matrix from the similarity matrix. A
user-friendly tutorial of this algorithm is in
[A Tutorial on Spectral Clustering](https://arxiv.org/pdf/0711.0189.pdf).
After one has obtained the eigenvectors of the Laplacian matrix, one use the 
corresponding values of a specific sample in each eigenvectors as the embedded
coordinate of the sample in a low dimensional space and visually inspect this 
embedded manifold.

With this package, this is finished in this following way.

### Start a new project
This package organize each different applications with a specified project folder.
```bash
ssh psana
cd /reg/neh/home5/haoyuan/Documents/my_repo/DiffusionMap
python start_a_new_project.py
```
If is this is the first time you execute these command lines, then you would see a
new folder called proj_000 appearing in the repo folder. "000" here represents the id
of this project. The script will automatically adjust this number to avoid the same 
id under this repo folder. 

Attention!

This script only avoid the same id under this repo folder. When you copy this project
folder to your own address, you might want to track the id number more carefully.

### Specify the parameters
Assume that the experiment folder is `/experiment/scratch` and that 
the username is `hahaha`. Then one might want to move this project folder to this
scratch folder  

```bash
mv /reg/neh/home5/haoyuan/Documents/my_repo/DiffusionMap/proj_000 /experiment/scratch/hahaha/
cd /experiment/scratch/hahaha/ 
```
One would find three folders under this folder.

    input
    output
    src
    
The input folder contains `file_list.txt` and `mask.npy`. One can specify which hdf5 
files to process or which datasets in which hdf5 files to process. More detailed 
explanations are given in the `file_list.txt`. The `mask.npy` is only a test file which
is most likely useless. You can specify your own mask file in a way which I'll explain
immediately.

By default, the `output` folder contains the results from this project. You can of
course change the output address in a way which I'll explain
immediately.

Inside the `src` folder, there are three python files.

    Config.py                  # To Spedify parameters.
    WeightMat.py               # To calculate the similarity matrix
    EigensSlepc.py             # To construct the symmetric Laplacian matrix
                               # and solve for the eigen-paires.
    
There are detailed explanations in the `Config.py` file about the function of each  
parameters. By changing the `mask_file` and `output_folder` values, you can easily 
switch to a new mask and new output folder.

### Calculate the similarity matrix.
Stay in the `/experiment/scratch/hahaha/src` folder.
Activate the official conda environment `ana-1.3.54`.
Acutally, any current `ana` environment should work.
Also, I would recommend `ana-1.3.54-py3` since officially
this package only support python3.

```bash
bsub -q psfehq -n 48 -R"span[ptile=1]" -o %J.out mpirun --mca btl ^openib python WeightMat.py
```

### Calculate the Laplacian matrix.
Stay in the `/experiment/scratch/hahaha/src` folder.
Activate the my personal conda environment.
```bash
conda activate /reg/neh/home/haoyuan/.conda/envs/mypython3
```
Due to a mismatch between the mpi4py in the official environment 
and the mpi4py required by packages `slec4py` and `petsc4py`, I have 
to use both the official environment to calculate the similarity matrix.

When you have acitvated my environment for this package, run
```bash
bsub -q psanaq -n 8 -R"span[ptile=1]" -o %J.out mpirun python EigensSlepc.py
```

### Visualization
Go to repo folder. Stay in my conda environment.
Open the jupyter notebook and have a look at the `Example_AMO86615.ipynb`.
There are detailed explanations in the notebook as to how to do the visualization.

To select a small region and see several randomly sampled patterns from that
region, use the box selection tool.

To select a small region and to save the index of all data points in the region,
use the polygon selection tool.

## Dependence
This package depends on the following packages

    python=3.6
    numpy
    hdf5
    dask
    scipy
    mpi4py
    holoviews
    pandas
    matplotlib
    jupyter notebook
    petsc4py
    slepc4py
 
This package has been tested only for python 3.6.
There's no guarantee on the result on the other python version. 

## Installation
This package has not been released at pip or conda yet. One has to first 
install all the dependence manually and then clone this repo. There
are several things to notice.

    1. To use petsc4py and slepc4py, one needs to make sure that 
       the mpi4py is the conda-forge version. i.e. intall the mpi4py with
       conda install -c conda-forge mpi4py
    2. At the beginning of the file WeightMat.py and EigensSlepc.py, I use
       sys.path to make sure that these two files can find the repo position.
       please modify these two values if you want to install your own version
       so that your scripts can find your repo.
    3. The jupyter notebook also has the previous dependence problem. The solution
       is again to modify sys.path at the beginning of the notebook.  

    
  
## TODO
Things to do

    1. Remove the dependence with dask. I am currely using dask to control the IO.
       when applying masks or doing some other complicated modifications, dask can
       becomes clumsy.
    2. Improve the visualization.
    3. To enable the user to tune the normalization methods when constructing
       the Laplacian matrix
       




