# Compute the surface temperature in ºC using B10 Landsat-8 data

# import required libraries
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def  compute_surface_temperature(file_path):
    # Reading data
    ds = gdal.Open(file_path)
    data = ds.ReadAsArray()

    # Create an empty array for temperatures
    rows, cols = data.shape
    temperatureData = np.zeros((rows, cols))

    # Iterate through each pixel in the image
    for i in range(rows):
        for j in range(cols):
            # Compute and store temp values
            if data[i,j] == 0:
                newVal = 0
            else:
                newVal = 0.00341802* data[i,j] + 149.0 # Kelvin
                newVal -= 273.15  # to Celsius
            temperatureData[i,j] = newVal

    # The Array Way
    # temperature_K = data*0.00341802+149.0
    # temperatureData = temperature_K-273.15

    # Create a figure with gridspec to place heatmap and histogram side by side
    fig = plt.figure(figsize=(10, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])  # 4:1 ratio for heatmap and histogram

    # Plot heatmap in the first subplot
    ax0 = plt.subplot(gs[0])
    heatmap = ax0.imshow(temperatureData, cmap='plasma')
    plt.colorbar(heatmap, ax=ax0, label='Temperature ($^\circ C$)')
    ax0.set_title('LandSat-8 Heatmap')

    # Plot histogram in the second subplot
    ax1 = plt.subplot(gs[1])
    ax1.hist(temperatureData[temperatureData > 0].ravel(), bins=np.arange(np.min(temperatureData), np.max(temperatureData)+0.1, 0.1), orientation='horizontal', color='orange')
    ax1.set_title('Distribution')
    ax1.set_xlabel('Frequency')
    # ax1.set_xscale('log')
    ax1.grid(True)

    # Save the figure with the heatmap and histogram
    plt.tight_layout()
    plt.savefig(f'tempFig_{file_path.replace("/", "-").replace(".", "")}')
    print(f'Saved as\ttempFig_{file_path.replace("/", "-").replace(".", "")}')
    plt.show()




# SAMPLE
# # island volcano
# 'IS_LANDSAT_8-LC08_L2SP_220015_20230718_20230802_02_T1_ST_B10.TIF',
# 'IS_LANDSAT_8-LC08_L2SP_221015_20240422_20240430_02_T1_ST_B10.TIF',

# # la palma island
# 'LP_LANDSAT_8-LC08_L2SP_207040_20231230_20240109_02_T1_ST_B10.TIF',

# # munich
# 'MU_LANDSAT_8/LC08_L2SP_193026_20240129_20240207_02_T1_ST_B10.TIF',

# # shanghai
# 'SH_LANDSAT_8-LC08_L2SP_118040_20240811_20240815_02_T1_ST_B10.TIF',
# 'SH_LANDSAT_8-LC08_L2SP_121038_20240901_20240906_02_T1_ST_B10.TIF',

# # random
# 'LC08_L2SP_193026_20240824_20240831_02_T1_ST_B10.TIF'




# SINGLE FILE
file_path = './SH_LANDSAT_8/LC08_L2SP_121038_20240901_20240906_02_T1_ST_B10.TIF'
compute_surface_temperature(file_path)




# MULTIPLE FILES
# files = ['IS_LANDSAT_8/LC08_L2SP_220015_20230718_20230802_02_T1_ST_B10.TIF',
#         'IS_LANDSAT_8/LC08_L2SP_221015_20240422_20240430_02_T1_ST_B10.TIF',
#         'LP_LANDSAT_8/LC08_L2SP_207040_20231230_20240109_02_T1_ST_B10.TIF',
#         'MU_LANDSAT_8/LC08_L2SP_193026_20240129_20240207_02_T1_ST_B10.TIF',
#         'SH_LANDSAT_8/LC08_L2SP_118040_20240811_20240815_02_T1_ST_B10.TIF',
#         'SH_LANDSAT_8/LC08_L2SP_121038_20240901_20240906_02_T1_ST_B10.TIF',
#         'LC08_L2SP_193026_20240824_20240831_02_T1_ST_B10.TIF']
    
# for file_path in files:
#     compute_surface_temperature(file_path)