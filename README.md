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

# ndfd_get_sco_data_script.py

This script grabs *historic* NDFD data from the North Carolina State Climate Office (SCO) THREDDS Server (TDS) for a specified past date. The original NDFD binary (.bin) file is converted to a panadas dataframe with the option to save total probability of precipitation for the next 12 hours (pop12) data and/or total accumulation of precipitation for the last 6 hours (i.e., quantitative precipitation frequency; qpf) data to a local directory as a .csv file. The units for pop12 are % and the units for qpf are km/m2, which can be converted to inches.

# ndfd_historic_forecast_analysis_script.R

This script takes locally stored data outputs from ndfd_get_sco_data_script.py, wrangles it, and plots it.