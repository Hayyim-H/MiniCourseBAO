# MiniCourseBAO
Short talk given by @hugoriv18 and @Hayyim-H for the BAO physics and its numerical implementation.

## Prerequisites

This course uses different python packages incompatibles with Windows, so it is imperative to use Linux or MacOS, or Windows with a Virtual Machine. Another requirement is having conda. 

### Installation:

Before doing anything, it is necessary to install the parallelization packages for your specific OS:
```bash
 # MacOS
 conda install -y -c conda-forge llvm-openmp gsl
#
```bash
 # Debian based Linux (Ubuntu/Mint/CentOS)
 conda install -y -c conda-forge libgomp gsl
#
Once 
