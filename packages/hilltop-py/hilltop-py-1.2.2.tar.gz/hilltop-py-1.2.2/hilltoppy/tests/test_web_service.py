# -*- coding: utf-8 -*-
"""
Created on Wed May 30 12:05:46 2018

@author: MichaelEK
"""
from hilltoppy.web_service import measurement_list, site_list, get_data, wq_sample_parameter_list

### Parameters
base_url = 'http://wateruse.ecan.govt.nz'
hts = 'WQAll.hts'
site = 'BV24/0024'
measurement = 'Nitrate Nitrogen'
from_date = '2015-01-01'
to_date = '2017-01-01'

### Tests


def test_site_list():
    sites = site_list(base_url, hts)
    assert len(sites) > 1000


def test_measurement_list():
    mtype_df1 = measurement_list(base_url, hts, site)
    assert len(mtype_df1) > 30


def test_wq_sample_parameter_list():
    mtype_df2 = wq_sample_parameter_list(base_url, hts, site)
    assert len(mtype_df2) > 10


def test_get_data1():
    tsdata1 = get_data(base_url, hts, site, measurement, from_date=from_date, to_date=to_date)
    assert len(tsdata1) > 5


def test_get_data2():
    tsdata2, extra2 = get_data(base_url, hts, site, measurement, from_date=from_date, to_date=to_date, parameters=True)
    assert (len(tsdata2) > 5) & (len(extra2) > 30)


def test_get_data3():
    tsdata3 = get_data(base_url, hts, site, 'WQ Sample', from_date=from_date, to_date=to_date)
    assert len(tsdata3) > 100

