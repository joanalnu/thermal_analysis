import pytest
import numpy as np
from osgeo import gdal
from thermal_analysis import compute_surface_temperature, generate_histogram, generate_heatmap

# Sample TIF file path
SAMPLE_TIF_PATH = 'test-example.TIF'

def test_compute_surface_temperature_valid():
    """Test valid temperature computation using the sample TIF file."""
    metaData, temperatureData = compute_surface_temperature(SAMPLE_TIF_PATH, degree='celsius')

    # Check if the returned temperatureData is a numpy array
    assert isinstance(temperatureData, np.ndarray)

    # Check if the shape of the temperatureData matches the input data
    ds = gdal.Open(SAMPLE_TIF_PATH)
    data = ds.ReadAsArray()
    assert temperatureData.shape == data.shape

def test_compute_surface_temperature_invalid_file():
    """Test handling of invalid file."""
    with pytest.raises(RuntimeError):
        compute_surface_temperature('invalid/path/to/file.tif')

def test_compute_surface_temperature_non_2d_array():
    """Test handling of non-2D array."""
    # Mock a non-2D array
    data = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        compute_surface_temperature(data)

def test_generate_histogram():
    """Test histogram generation."""
    data = np.array([[1, 2], [3, 4]])
    bins = np.arange(0, 5, 1)
    try:
        generate_histogram(data, bins, color='blue', grid=True, title='Test Histogram', xlabel='Value')
    except Exception as e:
        pytest.fail(f"generate_histogram raised an exception: {e}")

def test_generate_heatmap():
    """Test heatmap generation."""
    data = np.array([[25, 30], [35, 40]])  # Sample data
    try:
        generate_heatmap(data, 'test_heatmap.png', histo=True, histo_bins=10)
    except Exception as e:
        pytest.fail(f"generate_heatmap raised an exception: {e}")

def test_generate_heatmap_invalid_bins():
    """Test handling of invalid histogram bins."""
    data = np.array([[25, 30], [35, 40]])
    with pytest.raises(ValueError):
        generate_heatmap(data, 'test_heatmap.png', histo=True, histo_bins=-5)

def test_generate_heatmap_invalid_custom_range():
    """Test handling of invalid custom range."""
    data = np.array([[25, 30], [35, 40]])
    with pytest.raises(ValueError):
        generate_heatmap(data, 'test_heatmap.png', custom_range=(30, 20))

if __name__ == '__main__':
    pytest.main()