# About This Project
The National Digital Forecast Database (NDFD) is stored in GRIB2 format on the [NDFD Server](https://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/), which keeps the NDFD GRIB2 files up-to-date and accessible. In many cases, you don't work with GRIB2 files directly--instead,  we convert them to NetCDF4 files (which are slightly more friendly). The conversion process can be a headache, though.

This set of functions makes working with GRIB2 files a little easier. It provides a way to get a list of available NDFD areas along with the forecast time ranges and variables available for each area. From these available parameters, we can download data directly from the NDFD servers and load individual variables into Pandas Dataframes. Variables are stored locally to make everything work a little faster.

This project works mainly with NDFD Grid Data, but NDFD Point Access Data is available through a series of XML calls. I'm not exactly sure what you need for your project, but I'd be happy to create an example using the Point Access Data portal. 

# Requirements
To download the necessary requirements, `git clone` this repository and run this command:
```python
pip install requirements.txt
```
This should work in a Conda environment to, but I'm not certain of that.

The `cfgrib` library, which we use to load GRIB2 files, may require [some additional tools](https://github.com/ecmwf/cfgrib) for setup. If you are running MacOS, you can install this extra stuff using this command:
```python
brew install eccodes
```
Or, if you use Conda for package management:
```python
conda install -c conda-forge eccodes
```
