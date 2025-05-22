import scipy.io as sio
import numpy as np
import os
import traceback

def save_data_to_mat(data, path, fname, IPT, mupulse, muid, discard_channels):
    try:
        old_ipt = data["IPTs"]
        old_fsmp = data["fsamp"]
        data["fsamp"] = old_fsmp.astype(np.float64)
        old_mupulse = data["MUPulses"]
        if IPT.shape[1] < IPT.shape[0]:
            IPT = IPT.T
        data["IPTs"] = IPT
        data["MUIDs"] = muid
        data["MUPulses"] = mupulse
        data["discardChannelsVec"] = discard_channels.astype(np.float64)
        full_path = os.path.join(path, fname)
        sio.savemat(full_path, data)
        print(f"Data saved to {full_path}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        raise e
