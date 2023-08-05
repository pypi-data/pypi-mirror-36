"""
Methods for importing data from the WIND spacecraft.
All data is publically available at ftp://spdf.gsfc.nasa.gov/pub/data/wind.
See https://wind.nasa.gov/data_sources.php for more information on different
data products.
"""
import pathlib as path

import pandas as pd
import numpy as np
import astropy.units as u
import cdflib
import datetime as dt
from collections import OrderedDict

from heliopy.data import util
from heliopy import config

data_dir = path.Path(config['download_dir'])
wind_dir = data_dir / 'wind'
use_hdf = config['use_hdf']
remote_wind_dir = 'ftp://spdf.gsfc.nasa.gov/pub/data/wind/'


def _load_wind_cdf(starttime, endtime, instrument, data_product,
                   fname, badvalues={}, units=None):

    relative_dir = path.Path(instrument) / data_product
    # Get directories and filenames
    dirs = []
    fnames = []
    daylist = util._daysplitinterval(starttime, endtime)
    for day in daylist:
        date = day[0]
        filename = 'wi_{}_{}{:02}{:02}_v[0-9][0-9]'.format(
            fname, date.year, date.month, date.day)
        fnames.append(filename)
        local_dir = relative_dir / str(date.year)
        dirs.append(local_dir)
    extension = '.cdf'
    local_base_dir = wind_dir
    remote_base_url = remote_wind_dir

    def download_func(*args):
        util._download_remote_unknown_version(*args)

    def processing_func(cdf):
        return util.cdf2df(cdf, 'Epoch', badvalues=badvalues)

    return util.process(dirs, fnames, extension, local_base_dir,
                        remote_base_url, download_func, processing_func,
                        starttime, endtime, units=units)


def swe_h1(starttime, endtime):
    """
    Import 'h1' (Bi-Maxwellian, Anisotropic Analysis of Protons and Alphas)
    solar wind ion data product from WIND.
    Parameters
    ----------
    starttime : datetime
        Interval start time.
    endtime : datetime
        Interval end time.
    Returns
    -------
    data : :class:`~sunpy.timeseries.TimeSeries`
    """
    instrument = 'swe'
    data_product = 'swe_h1'
    fname = 'h1_swe'
    badvalues = {'Proton_V_nonlin': 99999.9,
                 'Proton_sigmaV_nonlin': 99999.9,
                 'Proton_VY_nonlin': 99999.9,
                 'Proton_sigmaVY_nonlin': 99999.9,
                 'Proton_W_nonlin': 99999.9,
                 'Proton_sigmaW_nonlin': 99999.9,
                 'Proton_Wperp_nonlin': 99999.9,
                 'Proton_sigmaWperp_nonlin': 99999.9,
                 'Proton_Wpar_nonlin': 99999.9,
                 'Proton_sigmaWpar_nonlin': 99999.9,
                 'EW_flowangle': 99999.9,
                 'SigmaEW_flowangle': 99999.9,
                 'NS_flowangle': 99999.9,
                 'SigmaNS_flowangle': 99999.9,
                 'Alpha_V_nonlin': 99999.9,
                 'Alpha_sigmaV_nonlin': 99999.9,
                 'Alpha_VX_nonlin': 99999.9,
                 'Alpha_sigmaVX_nonlin': 99999.9,
                 'Alpha_VY_nonlin': 99999.9,
                 'Alpha_sigmaVY_nonlin': 99999.9,
                 'Alpha_VZ_nonlin': 99999.9,
                 'Alpha_sigmaVZ_nonlin': 99999.9,
                 'Alpha_W_nonlin': 99999.9,
                 'Alpha_sigmaW_nonlin': 99999.9,
                 'Alpha_Wperp_nonlin': 99999.9,
                 'Alpha_sigmaWperp_nonlin': 99999.9,
                 'Alpha_Wpar_nonlin': 99999.9,
                 'Alpha_sigmaWpar_nonlin': 99999.9,
                 'Alpha_Na_nonlin': 99999.9,
                 'Alpha_sigmaNa_nonlin': 99999.9,
                 'Proton_Wperp_moment': 99999.9,
                 'Proton_Wpar_moment': 99999.9,
                 'Alpha_Na_nonlin': 100000.0,
                 'Alpha_sigmaNa_nonlin': 100000.0}
    units = OrderedDict([('fit_flag', u.dimensionless_unscaled),
                         ('ChisQ_DOF_nonlin', u.dimensionless_unscaled)])
    return _load_wind_cdf(starttime, endtime, instrument,
                          data_product, fname, badvalues, units=units)


def swe_h3(starttime, endtime):
    """
    Import 'h3' solar wind electron data product from WIND.
    Electron pitch angle files providing electron fluxes at 30 directional bins
    relative to the instantaneous magnetic field direction at 13 different
    energy levels
    Parameters
    ----------
    starttime : datetime
        Interval start time.
    endtime : datetime
        Interval end time.
    Returns
    -------
    data : :class:`~sunpy.timeseries.TimeSeries`
    """
    relative_dir = path.Path('swe') / 'swe_h3'
    # Get directories and filenames
    dirs = []
    fnames = []
    units = OrderedDict([('Angle', u .deg),
                        ('Energy', u.eV),
                        ('df', u.cm/u.s)])
    daylist = util._daysplitinterval(starttime, endtime)
    for day in daylist:
        date = day[0]
        filename = 'wi_h3_swe_{}{:02}{:02}_v[0-9][0-9]'.format(
            date.year, date.month, date.day)
        fnames.append(filename)
        local_dir = relative_dir / str(date.year)
        dirs.append(local_dir)
    extension = '.cdf'
    local_base_dir = wind_dir
    remote_base_url = remote_wind_dir
    distkeys = []
    for i in range(0, 13):
        distkeys.append('f_pitch_E' + str(i).zfill(2))
    anglelabels = []
    for i in range(0, 30):
        anglelabels.append((i + 0.5) * np.pi / 30)
    timekey = 'Epoch'
    energykey = 'Ve'

    def download_func(*args):
        util._download_remote_unknown_version(*args)

    def processing_func(cdf):

        df = util.pitchdist_cdf2df(cdf, distkeys, energykey, timekey,
                                   anglelabels)
        df = df.reset_index(level=['Energy', 'Angle'])
        return df

    return util.process(dirs, fnames, extension, local_base_dir,
                        remote_base_url, download_func, processing_func,
                        starttime, endtime, units=units)


def mfi_h0(starttime, endtime):
    """
    Import 'mfi_h0' magnetic field data product from WIND.
    Parameters
    ----------
    starttime : datetime
        Interval start time.
    endtime : datetime
        Interval end time.
    Returns
    -------
    data : :class:`~sunpy.timeseries.TimeSeries`
    """
    units = OrderedDict([('Bx_gse', u.nT), ('By_gse', u.nT),
                        ('Bz_gse', u.nT)])
    ignore = ['Time3_PB5']
    return _mfi(starttime, endtime, 'h0', units=units, ignore=ignore)


def mfi_h2(starttime, endtime):
    """
    Import 'mfi_h2' magnetic field data product from WIND.
    The highest time resolution data (11 vectors/sec usually, and
    22 vectors/sec when near Earth)
    Parameters
    ----------
    starttime : datetime
        Interval start time.
    endtime : datetime
        Interval end time.
    Returns
    -------
    data : :class:`~sunpy.timeseries.TimeSeries`
    """
    units = OrderedDict([('Bx_gse', u.nT), ('By_gse', u.nT),
                        ('Bz_gse', u.nT)])
    ignore = ['Time_PB5']
    return _mfi(starttime, endtime, 'h2', units=units, ignore=ignore)


def _mfi(starttime, endtime, version, units=None, ignore=None):
    """
    Import mfi magnetic field data products from WIND.
    Parameters
    ----------
    starttime : datetime
        Interval start time.
    endtime : datetime
        Interval end time.
    Returns
    -------
    data : DataFrame
    """
    # Directory relative to main WIND data directory
    relative_dir = path.Path('mfi') / ('mfi_' + version)
    # Get directories and filenames
    dirs = []
    fnames = []
    epoch_dict = {'h0': 'Epoch3', 'h2': 'Epoch'}
    mag_dict = {'h0': 'B3GSE', 'h2': 'BGSE'}

    epoch_key = epoch_dict[version]
    mag_key = mag_dict[version]

    keys = {mag_key: ['Bx_gse', 'By_gse', 'Bz_gse'],
            epoch_key: 'Time'}
    daylist = util._daysplitinterval(starttime, endtime)
    for day in daylist:
        date = day[0]
        # Absolute path to local directory for this data file
        local_dir = relative_dir / str(day[0].year)
        dirs.append(local_dir)
        filename = 'wi_' + version + '_mfi_' +\
            str(date.year) +\
            str(date.month).zfill(2) +\
            str(date.day).zfill(2) +\
            '_v[0-9][0-9]'
        fnames.append(filename)

    extension = '.cdf'
    local_base_dir = wind_dir
    remote_base_url = remote_wind_dir

    def download_func(*args):
        util._download_remote_unknown_version(*args)

    def processing_func(cdf):
        epoch_dict = {'h0': 'Epoch3', 'h2': 'Epoch'}
        epoch_key = epoch_dict[version]

        badvalues = {'Bx_gse': -1e+31,
                     'By_gse': -1e+31,
                     'Bz_gse': -1e+31}
        df = util.cdf2df(cdf, index_key=epoch_key,
                         badvalues=badvalues, ignore=ignore)
        return df

    return util.process(dirs, fnames, extension, local_base_dir,
                        remote_base_url, download_func, processing_func,
                        starttime, endtime, units=units)


def threedp_pm(starttime, endtime):
    """
    Import 'pm' WIND data.

    3 second time resolution solar wind proton and alpha particle moments from
    the PESA LOW sensor, computed on-board the spacecraft.

    Parameters
    ----------
    starttime : datetime
        Interval start time.
    endtime : datetime
        Interval end time.

    Returns
    -------
    data : :class:`~sunpy.timeseries.TimeSeries`
    """
    # Directory relative to main WIND data directory
    relative_dir = path.Path('3dp') / '3dp_pm'
    daylist = util._daysplitinterval(starttime, endtime)
    ignore = ['TIME']
    dirs = []
    fnames = []
    units = OrderedDict([('P_DENS', u.cm**-3),
                         ('P_VELS', u.km / u.s),
                         ('P_TEMP', u.eV),
                         ('A_DENS', u.cm**-3),
                         ('A_VELS', u.km / u.s),
                         ('A_TEMP', u.eV),
                         ('GAP', u.dimensionless_unscaled),
                         ('E_RANGE', u.eV),
                         ('VALID', u.dimensionless_unscaled),
                         ('VC', u.dimensionless_unscaled),
                         ('SPIN', u.dimensionless_unscaled)])
    extension = '.cdf'
    for day in daylist:
        date = day[0]
        this_relative_dir = relative_dir / str(day[0].year)
        filename = 'wi_pm_3dp_' +\
            str(date.year) +\
            str(date.month).zfill(2) +\
            str(date.day).zfill(2) +\
            '_v[0-9][0-9]'
        fnames.append(filename)
        dirs.append(this_relative_dir)

    local_base_dir = wind_dir
    remote_base_url = remote_wind_dir

    def download_func(*args):
        util._download_remote_unknown_version(*args)

    def processing_func(cdf):
        return util.cdf2df(cdf, 'Epoch', ignore=ignore)

    return util.process(dirs, fnames, extension, local_base_dir,
                        remote_base_url, download_func, processing_func,
                        starttime, endtime, units=units)


def threedp_sfpd(starttime, endtime):
    """
    Import 'sfpd' wind data.
    12 second energetic electron pitch-angle energy spectra from the foil SST
    Parameters
    ----------
    starttime : datetime
        Interval start time.
    endtime : datetime
        Interval end time.
    Returns
    -------
    data : :class:`~sunpy.timeseries.TimeSeries`
    """
    # Directory relative to main WIND data directory
    relative_dir = path.Path('3dp') / '3dp_sfpd'
    daylist = util._daysplitinterval(starttime, endtime)
    data = []
    fnames = []
    dirs = []
    units = OrderedDict([('Energy', u.eV),
                         ('Bx', u.nT),
                         ('By', u.nT),
                         ('Bz', u.nT),
                         ('Pitch angle', u.deg),
                         ('Flux', (u.cm**2 * u.sr * u.eV * u.s)**-1)])
    extension = '.cdf'
    for (date, _, _) in daylist:
        this_relative_dir = relative_dir / str(date.year)
        dirs.append(this_relative_dir)
        filename = 'wi_sfpd_3dp_{:{dfmt}}_v02'.format(
            date, dfmt='%Y%m%d')
        fnames.append(filename)

    local_base_dir = wind_dir
    remote_base_url = remote_wind_dir

    def download_func(*args):
        util._download_remote_unknown_version(*args)

    def processing_func(cdf):
        data_today = []
        # Loop through each timestamp to build up fluxes
        for non_empty_var in list(cdf.cdf_info().keys()):
            if 'variable' in non_empty_var.lower():
                if len(cdf.cdf_info()[non_empty_var]) > 0:
                    var_list = non_empty_var
                    break

        index_ = cdf.varget('Epoch')[...]
        index_ = cdflib.cdfepoch.breakdown(index_)
        index_ = np.asarray([dt.datetime(*x) for x in index_])
        energies_ = cdf.varget('ENERGY')[...]
        angles_ = cdf.varget('PANGLE')[...]
        fluxes_ = cdf.varget('FLUX')[...]
        magfield_ = cdf.varget('MAGF')[...]
        for i, time in enumerate(index_):
            energies = energies_[i, :]
            angles = angles_[i, :]
            fluxes = fluxes_[i, :, :]
            magfield = magfield_[i, :]
            index = pd.MultiIndex.from_product(
                ([time], energies, angles),
                names=['Time', 'Energy', 'Pitch angle'])
            df = pd.DataFrame(fluxes.ravel(), index=index, columns=['Flux'])
            df = df.reset_index(level=['Energy', 'Pitch angle'])
            df['Bx'] = magfield[0]
            df['By'] = magfield[1]
            df['Bz'] = magfield[2]
            data_today.append(df)
        data_today = pd.concat(data_today)
        data_today = data_today.sort_index()
        return data_today

    return util.process(dirs, fnames, extension, local_base_dir,
                        remote_base_url, download_func, processing_func,
                        starttime, endtime, units=units)
