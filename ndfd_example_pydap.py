#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20200410

@author: gray and sheila
"""

#%% Imports
import os
import re
from urllib.request import urlopen, urlretrieve, urlcleanup

import xarray as xr
import cfgrib
from pydap.client import open_url, open_file, open_dods # to convert bin file
import pandas as pd
import numpy as np

#%% Setup
#%%% Server Access
# These variables allow us to assemble a URL to access specific variables from
# the NDFD database. 
NDFD_SERVER = "http://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/"
NDFD_AREA = "AR.{}/"       # NDFD Area of Data
NDFD_TRNG = "VP.{}/"       # NDFD Valid Period (Forecast Time Range)
NDFD_VAR = "ds.{}.bin"     # NDFD Variable

#%%% Local Directories
DATA = "data/"

#%% Data Loading
def getNDFDlist(listof, area=None, timerange=None, ndfd_server=NDFD_SERVER):
    """
    Description: Returns a list of available NDFD parameters
    Parameters:
        listof (str): Either "areas", "timeranges", or "vars"
        area (str): Needed if listof="timeranges" or "vars"
        timerange (str): Needed if listof="vars"
        ndfd_server (str): URL to NDFD server with files 
    Returns:
        lines (list): List of extracted parameters
    """
    if listof == "areas":
        regex = r"(?<=a href=\"AR\.).*(?=\/\">)"
    elif listof == "timeranges":
        ndfd_server += NDFD_AREA.format(area)
        regex = r"(?<=a href=\"VP\.)\d\d\d\-\d\d\d(?=\/)"
    elif listof == "vars":
        ndfd_server += NDFD_AREA.format(area) + NDFD_TRNG.format(timerange)
        regex = r"(?<=a href=\"ds\.).*(?=\.bin\")"
    with urlopen(ndfd_server) as file:
        lines = file.readlines()
    lines = [line.decode("utf-8") for line in lines]
    lines = "\n".join(lines)
    lines = re.findall(regex, lines)
    urlcleanup()
    return lines

def getVariablePath(area, timerange, var):
    """
    Description: Assembles a directory and path for a specific NDFD variable 
    Parameters:
        area (str): Data area
        timerange (str): Forecast range (001-003, 004-007, or 008-450)
        var (str): Variable to access
    Returns:
        filepath (str): Path to local file with variable
    """
    area_url = NDFD_AREA.format(area)
    timerange_url = NDFD_TRNG.format(timerange)
    filedir = DATA + area_url + timerange_url
    filepath = filedir + var + ".bin"
    return filedir, filepath

def getVariable(area, timerange, var):
    """
    Description: Saves an NDFD variable to a local file, also returns remote url
    Parameters:
        area (str): Data area
        timerange (str): Forecast range (001-003, 004-007, or 008-450)
        var (str): Variable to access
    Returns:
        filepath (str): Path to local file with variable
    """
    area_url = NDFD_AREA.format(area)
    timerange_url = NDFD_TRNG.format(timerange)
    var_url = NDFD_VAR.format(var)
    remote_url = NDFD_SERVER + area_url + timerange_url + var_url
    
    filedir, filepath = getVariablePath(area, timerange, var)
    os.makedirs(filedir, exist_ok=True)
    
    filename, _ = urlretrieve(remote_url, filename=filepath)
    urlcleanup()
    return filename, remote_url

def getVariables(area_list, timerange_list, var_list):
    """
    Description: Saves a list of NDFD variables 
    Parameters:
        area (str list): Data area
        timerange (str list): Forecast range (001-003, 004-007, or 008-450)
        var (str list): Variable to access
    Returns:
        filepaths (list): Path to local file with variable
        remote_urls (list): Remote urls to variable
    """
    filepaths = []
    remote_urls = []
    for area in area_list:
        for timerange in timerange_list:
            for var in var_list:
                filepath, remote_url = getVariable(area, timerange, var)
                filepaths.append(filepath)
                remote_urls.append(remote_url)
    return filepaths, remote_urls

# %%
# might not need this fucntion (?)
def loadVariable(area, timerange, var):
    """
    Description: Loads an NDFD variable into the workspace as an xarray 
    Parameters:
        area (str): Data area
        timerange (str): Forecast range (001-003, 004-007, or 008-450)
        var (str): Variable to access
    Returns:
        ndfd_variable_xr (xarray): An xarray dataset
        ndfd_variable_pd (pandas): A pandas dataframe
    """
    filedir, filepath = getVariablePath(area, timerange, var)
    if not os.path.exists(filepath):
        getVariable(area, timerange, var)
    ndfd_variable_xr = xr.open_dataset(filepath, engine="cfgrib")
    ndfd_variable_pd = ndfd_variable_xr.to_dataframe()
    return ndfd_variable_xr, ndfd_variable_pd

# %% testing out functions

# list of areas
ndfd_areas = getNDFDlist(listof = "areas", ndfd_server = NDFD_SERVER)

# list of variables for 1-3 days in the Mid Atlantic
ndfd_vars = getNDFDlist(listof = "vars", area = "midatlan", timerange = "001-003", ndfd_server = NDFD_SERVER)

# get bin file filename and remote_url
ndfd_midatlan_pop12_filename, ndfd_midatlan_pop12_remote_url = getVariable("midatlan", "001-003", "pop12")

# read in file
ndfd_midatlan_pop12_bin = open_url(ndfd_midatlan_pop12_remote_url)
# ndfd_midatlan_pop12_bin = open_url(ndfd_midatlan_pop12_remote_url, output_grid = False)
# ndfd_midatlan_bin = open_url("http://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/VP.001-003/")

# this isn't working...maybe it has to be a TDS server url?
# some help? https://www.pydap.org/en/latest/client.html

