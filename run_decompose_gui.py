#!/usr/bin/env python3
"""
Sample script demonstrating EMG decomposition with waveform visualization.
"""

import os
from emgdecomp.decomposition import EmgDecomposition
from emgdecomp.parameters import EmgDecompositionParams
from tools import flatten_signal, discardChannels, setup_logger, bandpass_filter
import numpy as np
import scipy.io as sio
import numpy as np
from guis import select_action, select_folder, find_mat_files, select_files_from_list
import traceback
import dataclasses
from mat_assistant import save_data_to_mat

# Define paths relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, 'sample1.mat')
output_file = os.path.join(script_dir, 'sample1_decomposed')
ica_file = os.path.join(script_dir, 'sample1_ica.npz')
scores_file = os.path.join(script_dir, 'sample1_scores.npz')



def main():
    try:
        logger = setup_logger(name=__name__)
        actions = select_action()
        # print(f"Actions: {actions}")
        if len(actions) == 0:
            logger.info("No actions selected")
            return
        else:
            save_path = select_folder("Select the folder to save the results")
            if save_path is None:
                save_path = os.path.join(os.path.dirname(__file__), "results")
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
            if "decompose" in actions:
                lowcut = 10
                highcut = 900
                order = 6
                bandpass = True

                folder_path = select_folder("Select the folder containing the EMG data")
                mat_files = find_mat_files(folder_path)
                logger.info(f"Found {len(mat_files)} mat files in the folder")
                selected_files = select_files_from_list(mat_files)
                logger.info(f"Selected files: {selected_files}")
                for file in selected_files:
                    
                    full_file_path = os.path.join(folder_path, file)
                    logger.info(f"Decomposing {full_file_path}")
                    data = sio.loadmat(full_file_path)
                    emg = data["SIG"]
                    discard = data["discardChannelsVec"]
                    fsamp = data["fsamp"].item()
                    flattened_emg = flatten_signal(emg)
                    channels_to_discard = flatten_signal(discard)
                    channels_to_discard = channels_to_discard[1:]
                    flattened_emg = discardChannels(flattened_emg, channels_to_discard)
                    flattened_emg = bandpass_filter(flattened_emg)
                    params = EmgDecompositionParams(
                        sampling_rate=fsamp,
                        extension_factor=15,
                        maximum_num_sources=150,
                        min_peaks_distance_ms=5,
                        contrast_function='cube',
                        max_iter=100
                    )
                    decomp = EmgDecomposition(params=params)
                    IPTs, MUid, MUpulses, Threshold= decomp.decompose(flattened_emg)
                    fname = file[:-4] + "_I150_emgdecomp.mat"
                    save_data_to_mat(data, save_path, fname, IPTs, MUpulses, MUid, discard)
    except FileNotFoundError as e:
        print(e)
        traceback.print_exc()
        raise e



if __name__ == '__main__':
    # main()
    # Uncomment to load saved results instead of recomputing
    # load_saved_results()
    # mat_file = r"F:\7_MU Edit\opensource data\GL_10_seg.mat"
    # load_and_preprocess_emg_from_demuse(mat_file)
    main()

    # config = DecomposeParams()
    # print(config.lowcut)
    # print(config.highcut)
    # print(config.order)
    # print(config.bandpass)
    # print(config.M)
    # print(config.Refinements)
    # print(config.threshold)
    # print(config.method)

    # config2 = DecomposeParams(a = 10)
    # print(config2.lowcut)
    # print(config2.highcut)
    # print(config2.order)
    # print(config2.bandpass)
    # print(config2.M)
    # print(config2.Refinements)
    # print(config2.a)
