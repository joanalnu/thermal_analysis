# Compute LandSat-8 B10 temeprature band with big 
# Copyright: 2024 Joan Alcaide-Núñez. All rights reserved.

# import required libraries
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# define important paths
dirpath = os.path.dirname(os.path.abspath(__file__))
folders = [''] # Update with your folders
# Example 'LANDSAT8_B10_FOLDER' with any "/"

# iterate through folders
for folder in folders:
    abs_folderpath = f'{dirpath}/{folder}/' # define folder path
    filelist = [filename for filename in os.listdir(abs_folderpath) if 'metadata' not in filename] # list files
    for filename in filelist: #iterate through files

        # read data
        ds = gdal.Open(abs_folderpath+filename)
        print(f'This is the FILEPATH: {abs_folderpath+filename}')
        data = ds.ReadAsArray()

        # Create an empty array for temperatures
        rows, cols = data.shape
        temperatureData = np.zeros((rows, cols))

        # Iterate through each pixel in the image
        for i in range(rows):
            for j in range(cols):
                # compute and store temperature values
                if data[i,j]==0:
                    newVal = 0 # ignore blanck pixels
                else:
                    newVal = 0.00341802*data[i,j] + 149.0 # in Kelvin
                    newVal -= 273.15 # to Celsius

                    # This formula was extracted from email by Max and from metadata
                temperatureData[i,j] = newVal
        
        # Note that there is also an "Array-way", but it does not take into account blanck pixels
        # temperature_K = data*0.00341802+149.0
        # temperatureData = temperature_K-273.15

        # Create a figure with gridspec to place heatmap and histogram side by side
        fig = plt.figure(figsize=(10, 6))
        gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1]) # 4:1 ratio for heatmap and histogram

        # Plot heatmap in the first subplot
        ax0 = plt.subplot(gs[0])
        heatmap = ax0.imshow(temperatureData, cmap='plasma')
        plt.colorbar(heatmap, ax=ax0, label='Temperature (°C)')
        ax0.set_title('LandSat-8 Heatmap')

        # Plot histogram in the second subplot
        ax1 = plt.subplot(gs[1])
        ax1.hist(temperatureData[temperatureData>0].ravel(), bins=np.arrange(np.min(temperatureData), np.max(temperatureData)+0.1, 0.1), orientation='horizontal', color='orange')
        ax1.set_title('Distribution')
        ax1.set_xlabel('Frecuency')
        # ax1.set_xscale('log') # activate this to see weak signals (see histogram in logarthmic scale)
        ax1.grid(True)

        # Create a new directory inside the folder for saving the figures
        save_dir = os.path.join(abs_folderpath, 'temperature_analysis')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Define the file name for the saved figure
        save_path = os.path.join(save_dir, f'{os.path.splitext(filename)[0]}_analysis.png')

        # Save the figure
        plt.tight_layout()
        plt.savefig(save_path)

        # clear current figure to avoid overlapping problems
        plt.clf()