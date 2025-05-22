# Copyright (C) 2022 Daniel King, Jasmine Ortega, Rada Rudyak, Rowan Sivanandam
# This script contains functions that preprocess raw EMG data for input into
# the blind source separation algorithm.

from scipy import linalg
import scipy.io as sio
from scipy.signal import butter, lfilter
import numpy as np

def flatten_signal(raw):
    """
    Takes the raw EMG signal array, flattens it, and removes empty channels with no data.

    Parameters
    ----------
    raw: numpy.ndarray
        Raw EMG signal array.

    Returns
    -------
    numpy.ndarray
        Flattened EMG signal array, with empty channels removed.
    """
    # Flatten input array
    raw_flattened = raw.flatten()
    # Remove empty channels and then removes dimension of size 1
    raw_flattened = np.array(
        [channel for channel in raw_flattened if 0 not in channel.shape]
    ).squeeze()

    return raw_flattened


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


