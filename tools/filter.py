from scipy import linalg
from scipy.signal import butter, lfilter
import numpy as np

def butter_bandpass_filter(data, lowcut=10, highcut=900, fs=2048, order=6):
    """
    Filters input data using a Butterworth band-pass filter.

    Parameters
    ----------
        data: numpy.ndarray
            1D array containing data to be filtered.
        lowcut: float
            Lower range of band-pass filter.
        highcut: float
            Upper range of band-pass filter.
        fs: float
            Sampling frequency in Hz.
        order: int
            Order of filter.

    Returns
    -------
        numpy.ndarray
            Filtered data.

    Examples
    --------
        >>> butter_bandpass_filter(data, 10, 900, 2048, order=6)
    """
    
    b, a = butter(order, [lowcut, highcut], fs=fs, btype="band")
    filtered_data = lfilter(b, a, data)
    return filtered_data

def bandpass_filter(data, lowcut=10, highcut=600, fs=2048, order=6):
    """
    Apply bandpass filter to the data.
    """
    x = np.apply_along_axis(
        butter_bandpass_filter,
        axis=1,
        arr=data,
        lowcut=lowcut,
        highcut=highcut,
        fs=fs, 
        order=order)
    return x
