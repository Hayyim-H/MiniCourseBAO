# MiniCourseBAO
Short talk given by @hugoriv18 and @Hayyim-H for the BAO physics and its numerical implementation.

## Prerequisites

This course uses different python packages incompatibles with Windows, so it is imperative to use Linux or MacOS, or Windows with a Virtual Machine. Another requirement is having conda. 

### Enviroment installation:

Before doing anything, it is necessary to install the parallelization packages for your specific OS:
> MacOS
```bash
 conda install -y -c conda-forge llvm-openmp gsl
```
> Debian based Linux (Ubuntu/Mint/CentOS)
```bash
 conda install -y -c conda-forge libgomp gsl
```
Once you have that installed, you need to download the [environment.yml](Installation/environment.yml) file, which contains the python configuration to create the **BAOEnv** environment. You need to use 
```bash
 conda env create -f environment.yml
```

