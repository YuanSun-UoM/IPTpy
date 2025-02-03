# Source Data Download

------

## Global Anthropogenic Inventories

CESM's default anthropogenic emission data is based on [CEDSv2017_05_18](https://doi.org/10.5194/gmd-13-461-2020) over 1750-2100 for CMIP6, incorporating historical data up to 2014 and projection data from 2015 to 2100 under several SSP scenarios. Besides the default data, there is a rising need for using other inventories such as [CAMSv5.3](https://permalink.aeris-data.fr/CAMS-GLOB-ANT) and [CEDSv2021_04_21](https://data.pnnl.gov/dataset/CEDS-4-21-21). 

### Comparison of Global Anthropogenic Inventories

| Feature            | [CAMSv5.3](https://permalink.aeris-data.fr/CAMS-GLOB-ANT)    | [CEDSv2021_04_21](https://data.pnnl.gov/dataset/CEDS-4-21-21) |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Time step          | Monthly                                                      | Monthly                                                      |
| Period             | 2000-01-01 to present                                        | 1750-01-16 to 2019-12-16                                     |
| Version            | v5.3                                                         | v2021_04_21                                                  |
| Spatial resolution | 0.1°x0.1°                                                    | 0.5°x0.5°                                                    |
| Download method    | [Wget](https://permalink.aeris-data.fr/CAMS-GLOB-ANT)        | [Globus](https://www.globus.org/data-transfer)               |
| Required scripts   | [regrid.py](../../src/anthro_emission/fv/regrid.py), [rename.py](../../src/anthro_emission/fv/rename.py) | [sum.py](../../src/anthro_emission/fv/sum.py), [regrid.py](../../src/anthro_emission/fv/regrid.py), [rename.py](../../src/anthro_emission/fv/rename.py) |

## Download Data Manually 

### [CAMSv5.3](https://permalink.aeris-data.fr/CAMS-GLOB-ANT)

- Sign up and log in with your [ECCAD account](https://eccad.sedoo.fr).
- Go to the [CAMS-GLOB-ANT](https://eccad.sedoo.fr/#/metadata/479) webpage and click the **Go to Data** button on the top right corner.

<img src="../_static/images/download/CAMSv5.3/webpage.png" alt="webpage" width="100%">
<br><br>

- Enter the selection page and choose **CAMS** from DATASETS, **Anthropogenic** from CATEGORIES, **CAMS-GLOB-ANT** from DATASET, **V5.3** from SCENARIOS / VERSIONS, and groups or parameters you are interested in. Then, click the 'Add' button for download.

<img src="../_static/images/download/CAMSv5.3/datalist.png" alt="datalist" width="100%">
<br><br>

- After 'Add', the left bar shows added item. Then, click the 'Download' button at the top. 

<img src="../_static/images/download/CAMSv5.3/add.png" alt="add" width="100%">
<br><br>

- Select species, sectors, and file options:
  - For sectors, we only need to select **Sum Sectors** for most species while select all sectors for SO2. 
  - For file options, please select **1 file per year**, **Monthly**, Date (for example, 2000-01-01 to 2000-12-01), **flux (kg m-2 s-1)**.  Scroll down to the webpage bottom and click 'Download'.

<img src="../_static/images/download/CAMSv5.3/selection.png" alt="selection" width="100%">
<br><br>

-  Waite for the server to process your download request. After imformed by emails, turn to **My Downloads** of your account at the top right corner. 

<img src="../_static/images/download/CAMSv5.3/mydownload.png" alt="mydownload" width="100%">
<br><br>

- Click **Copy wget command** and past the command into your bash. The downloaded file is, for example, CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_propane_v5.3_monthly_2000.zip

  ```
  # Go to the directory for storing CAMS data, for example, 
  mkdir CAMS-GLOB-ANTv5.3
  cd CAMS-GLOB-ANTv5.3
  
  # Create a folder for the year 2000
  mkdir -p 2000
  
  # Below is an example of command line copied from the webpage. It should be expired over time. 
  wget --no-check-certificate -c -t 0 --timeout=60 --waitretry=300 --content-disposition https://api.sedoo.fr/eccad-download-rest/public/links/C2KHSnGmZ6
  
  # Unzip the downloaded file and get files for a single species by year 
  unzip CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_propane_v5.3_monthly.zip
  
  # Move files into the corresponding year folder
  mv CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_propane_v5.3_monthly/CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_propane_v5.3_monthly_2000.nc 2000/
  
  # delete zip files and empty folders if necessary
  rm -rf CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_propane_v5.3_monthly
  rm -rf CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_propane_v5.3_monthly.zip
  ```

  - Note that we download and save data by year. That is, the data directory structure should be restricted as:

    /

    │── 2000/

    │  ├── *_monthly_2000.nc

    │  ├── ......

    │── 2001/

    │  ├── *_monthly_2001.nc

    │  ├── ......

    │── ......

  - If the data directory is inconsistent as expected, the code would meet error of failing to find the data files.  

### [CEDSv2021_04_21](https://data.pnnl.gov/dataset/CEDS-4-21-21)

- Sign up and log in with your Globus account at the https://www.globus.org/
- Search **PNNL Data Hub** collection and click **Open in File Management** bottom on the right. 

<img src="../_static/images/download/CEDSv2021_04_21/pnnl.png" alt="pnnl" width="100%">
<br><br>

- Enter the **Path** on the left side, for example, /CEDS/CEDS_gridded_data_2021-04-21/data/BC/individual_files/ and select targeted files. For the right side, enter the collection of your destination. For example, we saved data to [JASMIN](https://jasmin.ac.uk/about/), an UK HPC supporting large-scale data analysis. Users could also save data to their local computer or other HPC platforms.

<img src="../_static/images/download/CEDSv2021_04_21/send.png" alt="send" width="100%">
<br><br>

- Keep the directory structure of downloaded data the same as the PNNL's.  Samely, if the data directory is inconsistent as expected, the code would meet error of failing to find the data files.  
- Alternatively, users can use the [GLOBUS command-line interface (CLI)](https://docs.globus.org/cli/) for data downloads, providing a reliable and high-performance transfer method. We provides a [bash job script](ceds.sh) for reference. 

