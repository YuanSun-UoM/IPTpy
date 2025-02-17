import os
import numpy as np
import pandas as pd
import xarray as xr
import datetime

class FV(object):
    """
    FV class for processing global anthropogenic emissions for the FV dynamic core in CESM.
    
    Parameters
    ----------
    start_year : int
        Starting year for processing.
    
    start_month : int
        Starting month for processing, default is 1.
    
    preregrid_path : str
        Path to pre-regridded data.

    regrided_path : str
        Path to regridded data.

    renamed_path : str
        Path to renamed data after regridding.

    end_year : int
        Ending year for processing.
    
    end_month : int
        Ending month for processing, default is 12.

    source : str, optional
        Data source.
    
    version : str, optional
        CEDS version, either is 'v5.3' for CAMS or 'v2021-04-21' for CEDS.
    
    timestep : str, optional
        Data timestep, default is 'monthly'.
    
    original_resolution : str, optional
        Original resolution of the data, either '0.1x0.1' for CAMS or '0.5x0.5' for CEDS.
    
    target_resolution : str, optional
        Target resolution for output, default is '0.9x1.25'.
    
    var_name : str, optional
        Variable name in output files, default is 'emiss_anthro'.

    cdate : str, optional     
        Creation date for output files, default is current date.
    """
    def __init__(self,
                 start_year: int,
                 end_year: int,
                 preregrid_path: str,
                 regridded_path: str,
                 renamed_path: str,
                 start_month: int = None,
                 end_month: int = None,
                 source: str = 'CEDS',
                 version: str = 'v2021-04-21',
                 timestep: str = 'monthly',
                 original_resolution: str = '0.5x0.5',
                 target_resolution: str = '0.9x1.25',
                 var_name: str = 'emiss_anthro',
                 cdate: str = None):
        """
        This is the __init__ method docstring for FV.
        """
        self._start_year = start_year
        self._end_year = end_year
        self._preregrid_path = preregrid_path
        self._regridded_path = regridded_path
        self._renamed_path = renamed_path
        for path in [preregrid_path, regridded_path, renamed_path]:
            if os.path.exists(preregrid_path) == False:
                os.makedirs(preregrid_path)
                print(f'Created directory {preregrid_path}')    
        self._source = source
        self._version = version
        self._timestep = timestep
        self._oriin
        self._target_resolution = target_resolution
        self._var_name = var_name
        self._sourcedata_var_list = sourcedata_var_list
        if cdate is None:
            self._cdate = datetime.datetime.now().strftime('%Y%m%d')
        else:
            self._cdate = cdate
        if source not in ['CEDS']:
            raise ValueError('source must be CEDS')   
        if target_resolution not in ['0.9x1.25']:
            raise ValueError('target_resolution must be 0.9x1.25')
        if version not in ['v2021-04-21']:
            raise ValueError('version must be v2021-04-21 for CEDS')
        if start_year > end_year:
            raise ValueError('start_year must be less than or equal to end_year')
        if start_year < 1750:
            raise ValueError('start_year must be greater than or equal to 1750')
        if end_year > 2020: 
            raise ValueError('end_year must be less than or equal to 2020 for CEDS')
        if start_month is None:
            self._start_month = 1
        else:
            self._start_month = start_month    
        if end_month is None:
            self._end_month = 12    
        else:
            self._end_month = end_month    
        if self._end_year + self._end_month/12 <= self._start_year + self._start_month/12:
            raise ValueError('end_year and end_month must be greater than start_year and start_month')             
    
    def sum_up(self,
               input_path: str,
               sourcedata_var_list: list = None,
               model_var_list: list = None):
        """
        Sum up CEDS anthropogenic emissions (monthly) before regriding.
        """
        self._input_path = input_path
        full_sourcedata_var_list = ['BC', 'CO', 'NH3', 'NOx', 'OC', 'SO2',
                              'VOC01-alcohols', 'VOC02-ethane', 'VOC03-propane', 'VOC04-butanes', 
                              'VOC05-pentanes', 'VOC06-hexanes-pl', 'VOC07-ethene', 'VOC08-propene',
                              'VOC09-ethyne', 'VOC12-other-alke', 'VOC13-benzene', 'VOC14-toluene',
                              'VOC15-xylene', 'VOC16-trimethylb', 'VOC17-other-arom', 'VOC18-esters',
                              'VOC19-ethers', 'VOC21-methanal', 'VOC22-other-alka', 'VOC23-ketones',
                              'VOC24-acids']
        # Mapping CEDS variables to model variables
        model_mapping = {
            'BC': 'bc', 'CO': 'co', 'NH3': 'nh3', 'NOx': 'nox', 'OC': 'oc', 'SO2': 'so2',
            'VOC01-alcohols': 'alcohols', 'VOC02-ethane': 'ethane', 'VOC03-propane': 'propane',
            'VOC04-butanes': 'butanes', 'VOC05-pentanes': 'pentanes', 'VOC06-hexanes-pl': 'hexanes',
            'VOC07-ethene': 'ethene', 'VOC08-propene': 'propene', 'VOC09-ethyne': 'ethyne',
            'VOC12-other-alke': 'other-alkenes-and-alkynes', 'VOC13-benzene': 'benzene', 'VOC14-toluene': 'toluene',
            'VOC15-xylene': 'xylene', 'VOC16-trimethylb': 'trimethylbenzene', 'VOC17-other-arom': 'other-aromatics',
            'VOC18-esters': 'esters', 'VOC19-ethers': 'ethers', 'VOC21-methanal': 'methanal',
            'VOC22-other-alka': 'other-aldehydes', 'VOC23-ketones': 'ketones', 'VOC24-acids': 'acids'
        }
        self._sourcedata_var_list = sourcedata_var_list
        self._model_var_list = [model_mapping[var] for var in sourcedata_var_list if var in model_mapping]
        # Default to full list if var_list is not provided
        if sourcedata_var_list is None:
            sourcedata_var_list = full_sourcedata_var_list
        
        # Validate the user-provided var_list
        invalid_vars = [var for var in sourcedata_var_list if var not in full_sourcedata_var_list]
        if invalid_vars:
            raise ValueError(f"Invalid variables in var_list: {invalid_vars}. "
                             f"Valid options are: {full_sourcedata_var_list}.")   
            print(f'Created directory {output_path}')
        if os.path.exists(input_path) == False:
            raise ValueError('input_path does not exist') 

        period_start_index = (self._start_year - 2000) * 12 + self._start_month - 1
        period_end_index = (self._end_year - 2000) * 12 + self._end_month - 1
        for source_var, model_var in zip(self._sourcedata_var_list, self._model_var_list):
            print(f'Summing up {source_var}')
            if source_var in ['BC', 'CO', 'NH3', 'NOx', 'OC', 'SO2']:
                filename = source_var + '-em-anthro'
                varname = source_var + '_em_anthro'
                data_path = self._input_path + source_var
                tag = '_gn_200001-201912.nc'
            else:
                filename = source_var + '-em-speciated-VOC-anthro'
                if source_var == 'VOC06-hexanes-pl':
                    data_path = self._input_path + 'VOC-speciated/VOC06-hexanes'
                elif source_var == 'VOC12-other-alke':   
                    data_path = self._input_path + 'VOC-speciated/VOC12-other'
                elif source_var == 'VOC17-other-arom':
                    data_path = self._input_path + 'VOC-speciated/VOC17-other'
                elif source_var == 'VOC22-other-alka':   
                    data_path = self._input_path + 'VOC-speciated/VOC22-other'  
                else:
                    data_path = self._input_path + 'VOC-speciated/' + source_var
                varname = source_var.replace("-", "_") + '_em_speciated_VOC_anthro'
                tag = '-supplemental-data_gn_200001-201912.nc'
            try:
                ds_path = f'{data_path}/individual_files/{filename}_input4MIPs_emissions_CMIP_CEDS-2021-04-21{tag}'
                ds_var = xr.open_dataset(ds_path)
            except FileNotFoundError:
                raise ValueError(f"File not found: {ds_path}")
                continue    
            ds_var_period = ds_var.sel(time=slice(ds_var.time[period_start_index], ds_var.time[period_end_index]))
            output_filename = f'{self._output_path}{model_var}_anthro_{self._start_year}{int(self._start_month):02d}16_{self._end_year}{int(self._end_month):02d}16_0.5_c{self._cdate}.nc'
            if os.path.exists(output_filename):
                os.remove(output_filename)
            renamed_da = ds_var_period[varname].sum(dim='sector').rename(self._var_name)
            renamed_da.attrs['long_name'] = ds_var_period[varname].attrs['long_name']
            renamed_da.attrs['units'] = ds_var_period[varname].attrs['units']
            renamed_da.attrs['cell_methods'] = ds_var_period[varname].attrs['cell_methods']
            renamed_da.to_netcdf(output_filename)
            print(f'Saved {output_filename}')
            # special handling for SO2 emissions (individual sectors)
            if source_var == 'SO2':
                print('Saving individual sector files for SO2')
                sector_list = ['agr', 'ene', 'ind', 'tra', 'res', 'sol', 'was', 'shp']
                for i, sector in enumerate(sector_list):
                    output_filename = f'{self._output_path}{model_var}_{sector}_anthro_{self._start_year}{int(self._start_month):02d}16_{self._end_year}{int(self._end_month):02d}16_0.5_c{self._cdate}.nc'
                    if os.path.exists(output_filename):
                        os.remove(output_filename)
                    renamed_da = ds_var_period[varname].sel(sector=i).rename(self._var_name)
                    renamed_da.attrs['long_name'] = ds_var_period[varname].attrs['long_name']
                    renamed_da.attrs['units'] = ds_var_period[varname].attrs['units']
                    renamed_da.attrs['cell_methods'] = ds_var_period[varname].attrs['cell_methods']
                    renamed_da.to_netcdf(output_filename)  

    def generate_regridder(self):
        """
        Generate regridder object for regridding CAMS or CEDS anthropogenic emissions to the CESM grid.
        """
        original_grid = xr.Dataset({'lat': self._original_lat, 'lon': self._original_lon})
        target_grid = xr.Dataset({'lat': self._target_lat, 'lon': self._target_lon})
        regridder = xe.Regridder(original_grid, target_grid, 'conservative', periodic=True)  
        if self._regridder_filename is None:
            print('Please provide a regridder_filename to save the regridder object.')
        if os.path.exists(self._regridder_filename):
            os.remove(self._regridder_filename)
            print(f'Removed existing regridder file {self._regridder_filename} and created a new one.')    
        regridder.to_netcdf(self._regridder_filename)

    def apply_regridder(self):
        """
        Apply regridder object to regrid CAMS or CEDS anthropogenic emissions to the CESM grid.
        """
        original_grid = xr.Dataset({'lat': self._original_lat, 'lon': self._original_lon})
        target_grid = xr.Dataset({'lat': self._target_lat, 'lon': self._target_lon})
        regridder = xe.Regridder(original_grid, target_grid, 'conservative', periodic=True, reuse_weights=True, weights=self._regridder_filename)
        for source_var, model_var in zip(self._sourcedata_var_list, self._model_var_list):
            print(f'Regridding {source_var} ...')
            if self._source == 'CAMS-GLOB-ANT':  
                date = '01'  
                dataset = []
                for year in range(self._start_year, self._end_year + 1):
                    # the CAMS data is downloaded and stored by year
                    ds = xr.open_dataset(f'{self._input_path}{year}/{self._source}_Glb_{self._original_resolution}_anthro_{source_var}_{self._version}_{self._timestep}_{year}.nc')
                    source_ds = ds['sum'].to_dataset(name=self._var_name)
                    rolled_source_ds = source_ds.roll(lon=1800, roll_coords=True)
                    rolled_source_ds['lon'] = xr.where(rolled_source_ds['lon'] < 0, 
                                                   rolled_source_ds['lon'] + 360, 
                                                   rolled_source_ds['lon'])
                    rolled_source_ds = rolled_source_ds.assign_coords(lon = self._original_lon, lat = self._original_lat)
                    regridded_ds = regridder(rolled_source_ds)
                    dataset.append(regridded_ds)
                output_ds = xr.concat(dataset, dim='time')
                sel_output_ds = output_ds.sel(time=slice(f'{self._start_year}-{self._start_month}-01', f'{self._end_year}-{self._end_month}-01'))
                output_filename = f'{self._output_path}{self._source}_{self._original_resolution}_anthro_{model_var}_{self._version}_{self._timestep}_{self._start_year}{int(self._start_month):02d}{date}_{self._end_year}{int(self._end_month):02d}{date}_{self._target_resolution}_c{self._cdate}.nc'
                if os.path.exists(output_filename):
                   os.remove(output_filename)
                sel_output_ds.to_netcdf(output_filename)
                if source_var == 'so2':
                    print('Regridding each sector for SO2 ...')
                    sector_list = ['awb', 'ene', 'fef', 'ind', 'ref', 'res', 'shp', 'swd', 'tnr', 'tro']
                    for sector in sector_list:
                        dataset = []
                        for year in range(self._start_year, self._end_year + 1):
                            ds = xr.open_dataset(f'{self._input_path}{year}/{self._source}_Glb_{self._original_resolution}_anthro_{source_var}_{self._version}_{self._timestep}_{year}.nc') 
                            source_ds = ds[sector].to_dataset(name=self._var_name)
                            rolled_source_ds = source_ds.roll(lon=1800, roll_coords=True)
                            rolled_source_ds['lon'] = xr.where(rolled_source_ds['lon'] < 0, 
                                           rolled_source_ds['lon'] + 360, 
                                           rolled_source_ds['lon'])
                            rolled_source_ds = rolled_source_ds.assign_coords(lon = self._original_lon, lat = self._original_lat)
                            regridded_ds = regridder(rolled_source_ds)
                            dataset.append(regridded_ds)
                        output_ds = xr.concat(dataset, dim='time')
                        output_filename = f'{self._output_path}{self._source}_{self._original_resolution}_anthro_{model_var}_{sector}_{self._version}_{self._timestep}_{self._start_year}{int(self._start_month):02d}{date}_{self._end_year}{int(self._end_month):02d}{date}_{self._target_resolution}_c{self._cdate}.nc'
                        if os.path.exists(output_filename):
                           os.remove(output_filename)
                        output_ds.to_netcdf(output_filename)
            elif self._source == 'CEDS':
                date = '16'
                ds = xr.open_dataset(f'{self._input_path}{model_var}_anthro_{self._start_year}{int(self._start_month):02d}{date}_{self._end_year}{int(self._end_month):02d}{date}_0.5_c{self._cdate}.nc')
                rolled_source_ds = ds.roll(lon=360, roll_coords=True)
                rolled_source_ds['lon'] = xr.where(rolled_source_ds['lon'] < 0, 
                                                   rolled_source_ds['lon'] + 360, 
                                                   rolled_source_ds['lon'])
                rolled_source_ds = rolled_source_ds.assign_coords(lon = self._original_lon, lat = self._original_lat)
                regridded_ds = regridder(rolled_source_ds)
                output_filename = f'{self._output_path}{self._source}_{self._original_resolution}_anthro_{model_var}_{self._version}_{self._timestep}_{self._start_year}{int(self._start_month):02d}{date}_{self._end_year}{int(self._end_month):02d}{date}_{self._target_resolution}_c{self._cdate}.nc'
                if os.path.exists(output_filename):
                    os.remove(output_filename)
                regridded_ds.to_netcdf(output_filename)
                if source_var == 'SO2':
                    print('Regridding each sector for SO2 ...')
                    sector_list = ['agr', 'ene', 'ind', 'tra', 'res', 'sol', 'was', 'shp']
                    for sector in sector_list:
                        ds = xr.open_dataset(f'{self._input_path}{model_var}_{sector}_anthro_{self._start_year}{int(self._start_month):02d}{date}_{self._end_year}{int(self._end_month):02d}{date}_0.5_c{self._cdate}.nc')
                        rolled_source_ds = ds.roll(lon=360, roll_coords=True)
                        rolled_source_ds['lon'] = xr.where(rolled_source_ds['lon'] < 0, 
                                                       rolled_source_ds['lon'] + 360, 
                                                       rolled_source_ds['lon'])
                        rolled_source_ds = rolled_source_ds.assign_coords(lon = self._original_lon, lat = self._original_lat)
                        regridded_ds = regridder(rolled_source_ds)
                        output_filename = f'{self._output_path}{self._source}_{self._original_resolution}_anthro_{model_var}_{sector}_{self._version}_{self._timestep}_{self._start_year}{int(self._start_month):02d}{date}_{self._end_year}{int(self._end_month):02d}{date}_{self._target_resolution}_c{self._cdate}.nc'
                        if os.path.exists(output_filename):
                            os.remove(output_filename)
                        regridded_ds.to_netcdf(output_filename)    



                 
                 
                 
                 
                 