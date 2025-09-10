import os


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