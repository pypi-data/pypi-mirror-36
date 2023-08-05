# PySide based visualization toolkit, PICViewer #

![picture](PICViewer_logo.png)

##The toolkit provides various easy-to-use functions for data analysis of PIC simulations.

## Main features
* 2D/3D openPMD or WarpX data visualization,
* multi-plot panels (up to 6 rows x 5 columns) controllable independently or synchronously,
* interactive mouse functions (panel selection, image zoom-in, local data selection, etc)
* animation from a single or multiple panel(s),
* saving your job configuration and loading it later,
* interface to use VisIt, yt, or mayavi for 3D volume rendering (currently updating)

## Required software
* python 2.7 or higher:
http://docs.continuum.io/anaconda/install.

* PySide
```
conda install -c conda-forge pyside
```
* h5py
* matplotlib
* numpy
* yt
* Numba

## To install manually

* Clone this repository `git clone https://jaehong2013@bitbucket.org/jaehong2013/picviewer.git`
* Switch to the cloned directory with `cd picviewer` and type `python setup.py install`
* Move on to a folder where your data files are located and type `picviewer` in the command line.

![picture](sample.png)
Figure shows several widget tools in the left side and multi-plot panels in the right side.
