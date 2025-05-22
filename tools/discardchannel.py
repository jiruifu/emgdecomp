import numpy as np


def discardChannels(data: np.ndarray, discard_channels: list[int]) -> np.ndarray:
    """
    Discard channels from the data array.
    Parameters
    ----------
    data: np.ndarray
        The flattened HD-EMG data. shape: (num_channels, num_samples)
    discard_channels: list[int]
        The channels to discard.
    Returns
    -------
    np.ndarray
        The data array with the specified channels discarded.
    """
    return np.delete(data, discard_channels, axis=0)

