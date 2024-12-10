# Create heat maps (surface temperature) in Degree Celcius using LandSat-8 B10 (TIR) data.
# Copyright: 2024 Joan Alcaide-Núñez. All rights reserved.

# import required libraries
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import thermal_analysis as ta

def compute_surface_temperature(file_path, degree='celcius'):
    # Reads raw data and compute surface temperature

    # Reading data
    try:
        ds = gdal.Open(file_path)
        if ds is None:
            raise FileNotFoundError(f"File not found or could not be opened: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error opening file: {e}")

    data = ds.ReadAsArray()
    if data is None:
        raise ValueError("The data could not be read from the file.")

    rows, cols = data.shape # read data shape
    rows, cols = data.shape
    if len(data.shape) != 2: # checking data is 2D
        raise ValueError("The data read from the file is not a 2D array.")
    temperatureData = np.zeros((rows, cols)) # create empty array

    # Iterate through each pixel in the image
    for i in range(rows):
        for j in range(cols):
            if not isinstance(data[i, j], (int, float)): # checking for invalid data types
                raise TypeError(f"Unexpected data type at pixel ({i}, {j}): {data[i, j]}")
            # Compute and store temp value
            if data[i,j] == 0: # fast-forwading zeros to avoid division by 0
                newVal = 0
            else:
                newVal = 0.00341802* data[i,j] + 149.0 # Kelvin (following LandSat-8 calibration docs)
                if degree in ['celcius', 'Celcius', 'CELCIUS']:
                    newVal -= 273.15 # to Celcius
                if degree in ['Fahrenheit', 'fahrenheit', 'FAHRENHEIT']:
                    newVal = (newVal -273.15) * 1.8 + 32 # to Fahrenheit
            temperatureData[i,j] = newVal

    # alternative array way (which does not account for zeros)
    # temperature_K = data*0.00341802+149.0
    # temperatureData = temperature_K-273.15

    metaData = [file_path, degree]
    return (metaData, temperatureData)

def generate_histogram(data, bins, color, grid, title, xlabel):
    # Generates a histogram for the given data.
    ax = plt.gca()  # Get the current axis
    ax.hist(data[data > 0].ravel(), bins=bins, orientation='horizontal', color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.grid(grid)

def generate_heatmap(data, file_path, dpi=300, cmap='plasma', title='LandaSat-8 Heatmap', grid=False, custom_range=(None, None),
                     histo=True, histo_color='orange', histo_grid=True, histo_title='Distribution', histo_bins=0.1):

    # Creates a matplotlib figure mapping surface temperature and optionally an accompanying histogram.

    fig = plt.figure(figsize=(10, 6))
    if histo:
        gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])  # 4:1 ratio for heatmap and histogram
        ax0 = plt.subplot(gs[0])
    else:
        ax0 = plt.subplot()

    # set vmin and vmax to image size if no input

    if custom_range[0] is None or custom_range[1] is None:
        vmin, vmax = np.nanmin(data), np.nanmax(data) # use nanmin and nanmax to handle NAN values
    else:
        if custom_range[0] >= custom_range[1]: # min can't be greater or equal than max
            raise ValueError("Invalid custom range: vmin must be less than vmax.")
        vmin, vmax = custom_range


    # Plot heatmap in the first subplot
    heatmap = ax0.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax) # if vmax and vmin is none it will raise a typeError
    plt.colorbar(heatmap, ax=ax0, label='Temperature ($^\circ C$)')
    ax0.set_title(title)
    ax0.grid(grid)

    if histo:
        # Plot histogram in the second subplot
        ax1 = plt.subplot(gs[1])
        plt.sca(ax1)  # Set the second subplot as the current axis
        bins = np.linspace(np.nanmin(data), np.nanmax(data), histo_bins) # compute bins for histogram
        if histo_bins <= 0: # checking bins is positive
            raise ValueError("Number of histogram bins must be a positive integer.")
        ta.generate_histogram(data, bins, color=histo_color, grid=histo_grid, title=histo_title)

    # Save the figure
    file_name = f'tempFig_{file_path.replace("/", "-").replace(".", "")}'
    plt.tight_layout()
    try:
        plt.savefig(file_name, dpi=dpi)
    except Exception as e:
        raise RuntimeError(f"Error saving the figure: {e}")
    print(f'Saved as\t{file_name}')
    plt.show()

# SINGLE FILE
file_path = './' + str(input('File path: '))
compute_surface_temperature(file_path)
# Example: LC08_L2SP_193026_20240824_20240831_02_T1_ST_B10.TIF


# MULTIPLE FILES
# files = [] # Update with your files
# Example: LC08_L2SP_193026_20240824_20240831_02_T1_ST_B10.TIF

# for file_path in files:
#     compute_surface_temperature('./'+file_path)