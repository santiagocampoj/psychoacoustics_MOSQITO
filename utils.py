import os
import argparse



def arg_parser():
    parser = argparse.ArgumentParser(description='Psychoacoustic Metrics Computation')
    parser.add_argument('-f', '--path_general', type=str, required=True, 
                        help='Path to Psychoacoustic wav folder')
    return parser.parse_args()


def mkdir_folder_wav_name(output_path, wav_name, png_string, folder_string):
    output_path_folder = os.path.join(output_path, f'{folder_string}')
    print(f"The output path for the signal plot is: {output_path_folder}")
    if not os.path.exists(output_path_folder):
        os.makedirs(output_path_folder)
        print(f"The output signal folder was created: {output_path_folder}")
    
    
    #adding the output_path_folder}") + wav_name + '_signal.png' to save the signal plot in the correct folder
    wav_name_path = os.path.join(output_path_folder, wav_name + f'{png_string}')
    print(f"The output path for the signal plot is: {wav_name_path}")

    
    return output_path_folder, wav_name_path



def to_jsonable(x):
    import numpy as np
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (list, tuple)):
        return [to_jsonable(i) for i in x]
    if isinstance(x, dict):
        return {k: to_jsonable(v) for k, v in x.items()}
    return x