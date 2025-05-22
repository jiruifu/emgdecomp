from tools import flatten_signal, discardChannels
import scipy.io as sio
import numpy as np

if __name__ == "__main__":
    path = r"F:\7_MU Edit\opensource data\GM_10_seg.mat"
    data = sio.loadmat(path)
    emg = data["SIG"]
    ch2discard = data["discardChannelsVec"]
    flattened_emg = flatten_signal(emg)
    channels_to_discard = flatten_signal(ch2discard)
    channels_to_discard = channels_to_discard[1:]
    print(channels_to_discard.shape)
    print(flattened_emg.shape)
    flattened_emg = discardChannels(flattened_emg, channels_to_discard)
    print(flattened_emg.shape)