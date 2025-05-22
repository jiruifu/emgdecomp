from emgdecomp.decomposition import EmgDecomposition
from emgdecomp.parameters import EmgDecompositionParams
from tools import flatten_signal, discardChannels
from scipy.io import loadmat
import numpy as np

path = r"F:\7_MU Edit\opensource data\GM_10_seg.mat"
SIG = loadmat(path)["SIG"]
ch2discard = loadmat(path)["discardChannelsVec"]

flattened_emg = flatten_signal(SIG)
channels_to_discard = flatten_signal(ch2discard)
channels_to_discard = channels_to_discard[1:]

flattened_emg = discardChannels(flattened_emg, channels_to_discard)

# fs = loadmat(path)["fsamp"].item()
# fs = fs.astype(np.int64)
# print(type(fs))

# path = r"F:\7_MU Edit\opensource data\GM_10_seg.mat"
# SIG = loadmat(path)["SIG"]
# ch2discard = loadmat(path)["discardChannelsVec"]

# flattened_emg = flatten_signal(SIG)
# channels_to_discard = flatten_signal(ch2discard)
# channels_to_discard = channels_to_discard[1:]

# flattened_emg = discardChannels(flattened_emg, channels_to_discard)

# # fs = loadmat(path)["fsamp"].item()
# # fs = fs.astype(np.int64)
# # print(type(fs))

params = EmgDecompositionParams(
    sampling_rate=float(loadmat(path)["fsamp"].item())
)

decomp = EmgDecomposition(params=params, use_cuda=True)
IPTs, MUid, MUpulses, Threshold= decomp.decompose(flattened_emg)


