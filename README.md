# Thermal Analysis
Computing surface temperature heatmaps using LandSat-8 publicly available images, based on GDAL Python Library.

[![repo](https://img.shields.io/badge/GitHub-thermal_analysis-blue.svg?style=flat)](https://github.com/joanalnu/thermal_analysis)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
<!--![Build Status](https://github.com/joanalnu/thermal_analysis/actions/workflows/python-tests.yml/badge.svg)
![Open Issues](https://img.shields.io/github/issues/joanalnu/thermal_analysis)-->

# Installation
To use the code in this repository you can clone it running the following command in your shell.
```bash
git clone https://github.com/joanalnu/thermal_analysis.git
```
Next, you can install it as a library using pip.
```bash
pip install thermal_analysis
```
Then you can import the code anywhere like
```python
import thermal_analysis as ta
```

# **Function Descriptions**

## **`compute_surface_temperature`**
- **Description:** Computes the surface temperature from a LandSat-8 satellite image.
- **Arguments:**
  - `file_path` (required): Path to a `.TIF` file containing the satellite image.
  - **Optional parameters:**
    - `degree`: Unit of temperature. Can be one of:
      - `'Celsius'` (default)
      - `'Kelvin'`
      - `'Fahrenheit'`
- **Returns:** A tuple composed by:
  - `metaData`: a list containing file name information and temperature unit.
  - `temperatureData`: a 2D array with the temperature values.

## **`generate_heatmap`**
- **Description:** Creates a heatmap to visualize temperature data using a color map.
- **Arguments:**
  - `data` (required): A NumPy array containing temperature values.
    - `colormap`: Specifies the color map to use (e.g., `'viridis'`, `'plasma'`, `'inferno'`, see [matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html)). Defaults to `'plasma'`.
    - `output_format`: Desired file format for the heatmap (e.g., `'png'`, `'jpeg', 'jpg', 'pdf'`). Defaults to `'png'`.
    - `title`: Title to display on the heatmap. Defaults to `LandSat-8 Heatmap`.
    - `label`: Label for the color bar. Defaults to `'Temperature (<unit>)'`.
    - `dpi`: Resolution of the output image. Defaults to `300`.
    - `grid`: Boolean to toggle gridlines. Defaults to `False`.
    - `custom_range`: Tuple specifying the (min, max) range of temperatures. Defaults to auto-scaling.
    - `histo`: Boolean to toggle a histogram to the side of the map. Defaults to `True`.
      - `histo_color`: Color of the histogram columns. Defaults to `orange`.
      - `histo_grid`: Boolean to toggle gridlines. Defaults to `True`
      - `histo_title`: Desired title for the histogram. Defaults to `'Distribution'`
      - `histo_bins`: Desired size of temperature bins for histogram. Defaults to `0.1`.
- **Returns:** Saves the heatmap as an image file.


# Copyright
#### **This repository is protected under the default copyright laws, meaning that the repository owner retains all the rights to this source code and no one may reproduce, distribute, or create derivative works from this work. [GitHub Licensing Notice](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)**

If you're are seeking to collaborate please refer to the [colaborating guidelines](https://github.com/joanalnu/thermal_analysis/.github/COLLABORATING.md). I'll be happy to get to know you and work together.

# Citation
Please, use this citation when referring to this repository, source code, modified and derivative versions of it.

```bibtex
@software{joanalnu_2024,
  author       = {Alcaide-Núñez, joan},
  title        = {joanalnu/thermal_analysis},
  month        = October,
  year         = 2024,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {},
  url          = {https://github.com/joanalnu/thermal_analysis}
}
```

# Acknowledge
I would like to thank Maximilan Langheinrich at IMF-DLR for feedback.

Also, I acknowledge the use of the following python libraries: gdal, numpy, matplotlib, and os

&copy; 2024 joanalnu (Joan Alcaide-Núñez). All rights reserved.