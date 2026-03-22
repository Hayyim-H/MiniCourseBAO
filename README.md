# MiniCourseBAO
Short talk given by @hugoriv18 and @Hayyim-H for the BAO physics and its numerical implementation.

## Prerequisites

This course uses different python packages incompatibles with Windows, so it is imperative to use Linux or MacOS, or Windows with a Virtual Machine. Another requirement is having conda. 

## Enviroment installation:

### For **Debian** based Linux (Ubuntu/Mint/CentOS):
You need to download the [environment_Linux.yml](Installation/environment_Linux.yml) file which contains the python configuration to create the **BAOEnv** environment. Then you only need to use
```bash
 conda env create -f environment_Linux.yml
```
### For **MacOS** with Apple Silicon:
The process it's different. First download the [environment_Mac.yml](Installation/environment_Mac.yml) file and use
```bash
 conda env create -f environment_Mac.yml
```
After that, you must navigate to the folder [Wheels/](Installation/Wheels/), activate the environment
```bash
 conda activate BAOEnv
```
and install those packages with
```bash
 pip install *.whl
```
If you are unable to install the environment then you can't run the notebook for @hugoriv18's talk. But you can create a new environment and install the basics for @Hayyim-H's talk with
```bash
 pip install cobaya getdist matplotlib
```
## Slides

https://docs.google.com/presentation/d/1TRyD4k_X_BrVIjiWdOBJnoWewKeuhG-9xx7ZNkE5VHg/edit?usp=sharing
