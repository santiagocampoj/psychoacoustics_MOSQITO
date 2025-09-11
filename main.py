# Add MOSQITO to the Python path
import os
import sys
sys.path.append('..')

# Import numpy
import numpy as np
# Import plot function
import matplotlib.pyplot as plt
# Import spectrum computation tool
from scipy.fft import fft, fftfreq
from scipy.signal import stft
# Import mosqito functions
from mosqito.utils import load

# LOUDNESS_ZWST functions
from mosqito.sq_metrics import loudness_zwst
from mosqito.sq_metrics import loudness_zwst_perseg
from mosqito.sq_metrics import loudness_zwst_freq


# ROUGHNESS_DW functions
from mosqito.sq_metrics import roughness_dw, roughness_dw_freq


# SHARPNESS_DIN functions
from mosqito.sq_metrics import sharpness_din_st
from mosqito.sq_metrics import sharpness_din_perseg
from mosqito.sq_metrics import sharpness_din_from_loudness
from mosqito.sq_metrics import sharpness_din_freq


# Import MOSQITO color sheme [Optional]
from mosqito import COLORS

# To get inline plots (specific to Jupyter notebook)
# %matplotlib notebook



import argparse
from tqdm import tqdm
import json
from logging_config import setup_logging
from config import *
from utils import *





def main():
    logger = setup_logging()
    args = arg_parser()
    logger.info("")
    logger.info("Starting psychoacoustic metrics computation")
    logger.info(f"Arguments: {args}")



    #setting the path
    folder_path = args.path_general
    mision_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]


    for folder in mision_folders:
        logger.info("")
        mission_path = os.path.join(folder_path, folder)

        #checking if they exit
        if os.path.exists(mission_path):
            logger.info(f"The folder exists: {mission_path}")


            for general_folder in GENERAL_FOLDERS:

                #5-RESULT FOLDER
                output_path = mission_path.replace("3-Medidas", "5-Resultados")
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                    logger.info(f"The output folder was created: {output_path}")
                else:
                    logger.info(f"The output folder already exists: {output_path}")
                logger.info("")

                #json output path
                json_output_path = os.path.join(output_path, f"{folder}_{general_folder}_metrics.json")
                logger.info(f"The JSON output path is: {json_output_path}")


                # GENERAL FOLDER (LOUDNESS_ZWST, ROUGHNESS_DW, SHARPNESS_DIN)
                general_analysis_folder = os.path.join(output_path, f'{general_folder}')
                logger.info(f"The output path is: {general_analysis_folder}")

                if not os.path.exists(general_analysis_folder):
                    os.makedirs(general_analysis_folder)
                    logger.info(f"The output folder was created: {general_analysis_folder}")
                else:
                    logger.info(f"The output folder already exists: {general_analysis_folder}")
                logger.info("")


                wav_files = [f for f in os.listdir(mission_path) if f.endswith('.wav')]
                for wav_file in wav_files:
                    logger.info("")
                    logger.info(f"Processing file: {wav_file}")


                    #initializin the results dictionary
                    results = {
                        "file": wav_file,
                        "metrics": {}
                    }



                    file_path = os.path.join(mission_path, wav_file)
                    wav_name = os.path.splitext(wav_file)[0]

                    # load signal
                    sig, fs = load(file_path, wav_calib=2 * 2 **0.5)
                    # plot signal
                    t = np.linspace(0, (len(sig) - 1) / fs, len(sig))
                    # exit()



                    if general_folder == LOUDNESS_ZWST_STRING:
                        logger.info("")
                        logger.info("ENTERING THE LOUDNESS_ZWST BLOCK")
                        _, loudness_zwst_signal_wav_name = mkdir_folder_wav_name(general_analysis_folder, wav_name, '_signal.png', 'Signal')
                        _, loudness_zwst_wav_name = mkdir_folder_wav_name(general_analysis_folder, wav_name, '_loudness_zwst.png', 'Loudness_Zwicker')
                        _, loudness_zwst_band_rate_wav_name = mkdir_folder_wav_name(general_analysis_folder, wav_name, '_loudness_zwst_band_rate.png', 'Loudness_Zwicker_Band_Rate')
                        _, loudness_zwst_segment_wav_name = mkdir_folder_wav_name(general_analysis_folder, wav_name, '_loudness_zwst_segment.png', 'Loudness_Zwicker_Segment')            
                        _, loudness_zwst_spectrum_wav_name = mkdir_folder_wav_name(general_analysis_folder, wav_name, '_loudness_zwst_spectrum.png', 'Loudness_Zwicker_Spectrum')



                        ###################################
                        ###################################
                        ###################################
                        ## SIGNAL ##
                        ###################################
                        ###################################
                        ###################################
                        logger.info("")
                        logger.info(f"Plotting signal for {wav_name}")
                        plt.figure(1)
                        plt.plot(t, sig, color=COLORS[0])
                        plt.xlabel('Time [s]')
                        plt.ylabel('Acoustic pressure [Pa]')
                        plt.title(f'Signal - {wav_name}')
                        plt.grid()

                        #SAVE
                        plt.savefig(loudness_zwst_signal_wav_name, dpi=300)
                        logger.info(f"Signal plot saved: {loudness_zwst_signal_wav_name}")
                        plt.close()
                        # break




                        # # ###################################
                        # # ###################################
                        # # ###################################
                        # # # COMPUTTING LOUDNESS ZWST
                        # # ###################################
                        # # ###################################
                        # # ###################################
                        logger.info("")
                        logger.info("Computing Loudness Zwicker")
                        N, N_specific, bark_axis = loudness_zwst(sig, fs, field_type="free")
                        results["metrics"]["loudness_zwst"] = {"global_loudness_sone": N,
                                                            # "specific_loudness_sone_per_bark": N_specific.tolist(),
                                                            # "bark_axis": bark_axis.tolist()
                                                            }
                        logger.info("N_zwst = {:.1f} sone".format(N))
                        # logger.info(f"N_zwst = {N:.1f} sone")

                        plt.figure(2)
                        plt.plot(bark_axis, N_specific, color=COLORS[0])
                        plt.xlabel("Critical band rate [Bark]")
                        plt.ylabel("N'_zwst [sone/Bark]")
                        plt.title(f"Loudness Zwicker - N_zwst = {N:.1f} sone - {wav_name}".format(N))
                        plt.grid()

                        # #SAVE
                        plt.savefig(loudness_zwst_wav_name, dpi=300)
                        logger.info(f"Loudness Zwicker plot saved: {loudness_zwst_wav_name}")
                        logger.info("")
                        plt.close()
                        



                        # ###################################
                        # ###################################
                        # ###################################
                        # # # SPECIFIC LOUDNESS OVER CRITICAL BAND RATE IS ALSO COMPUTED
                        # ###################################
                        # ###################################
                        # ###################################
                        logger.info("")
                        logger.info("Computing Loudness Zwicker - Specific Loudness over Critical Band Rate")
                        plt.figure(2)
                        plt.plot(bark_axis, N_specific, color=COLORS[0])
                        plt.xlabel("Critical band rate [Bark]")
                        plt.ylabel("N'_zwst [sone/Bark]")
                        plt.title(f"Loudness Zwicker - N_zwst = {N:.1f} sone - {wav_name}".format(N))
                        plt.grid()

                        # #SAVE
                        plt.savefig(loudness_zwst_band_rate_wav_name, dpi=300)
                        logger.info(f"Loudness Zwicker Band Rate plot saved: {loudness_zwst_band_rate_wav_name}")
                        logger.info("")
                        plt.close()



                        # ###################################
                        # ###################################
                        # ###################################
                        # # # SPECIFIC LOUDNESS PER SEGMENT
                        # ###################################
                        # ###################################
                        # ###################################
                        logger.info("")
                        logger.info("Computing Loudness Zwicker - Specific Loudness per Segment")
                        N, N_specific, bark_axis, time_axis = loudness_zwst_perseg(
                            sig, fs, nperseg=8192 * 2, noverlap=4096
                        )
                        results["metrics"]["loudness_zwst_per_segment"] = {
                            "global_loudness_sone_per_segment": N.tolist(),
                            # "specific_loudness_sone_per_bark_per_segment": N_specific.tolist(),
                            # "bark_axis": bark_axis.tolist(),
                            # "time_axis": time_axis.tolist()
                        }

                        #plotting
                        plt.figure(3)
                        plt.plot(time_axis, N, color=COLORS[0])
                        plt.xlabel("Time [s]")
                        plt.ylabel("N_zwst [sone]")
                        # plt.ylim((0, 15))
                        plt.title(f"Loudness Zwicker - {wav_name}")
                        plt.grid()

                        # # save
                        plt.savefig(loudness_zwst_segment_wav_name, dpi=300)
                        logger.info(f"Loudness Zwicker Segment plot saved: {loudness_zwst_segment_wav_name}")
                        logger.info("")
                        plt.close()



                        # ###################################
                        # ###################################
                        # ###################################
                        # # # FROM SPECTRUM
                        # ###################################
                        # ###################################
                        # ###################################
                        # # # Compute spectrum
                        logger.info("")
                        logger.info("Computing Loudness Zwicker from Spectrum")
                        n = len(sig)
                        spec = np.abs(2 / np.sqrt(2) / n * fft(sig)[0:n//2])
                        freqs = fftfreq(n, 1/fs)[0:n//2]
                        # Compute Loudness
                        N, N_specific, bark_axis = loudness_zwst_freq(spec, freqs)
                        results["metrics"]["loudness_zwst_from_spectrum"] = {
                            "global_loudness_sone": N,
                            # "specific_loudness_sone_per_bark": N_specific.tolist(),
                            # "bark_axis": bark_axis.tolist()
                        }

                        logger.info("N_zwst = {:.1f} sone".format(N) )



                        # plot
                        plt.figure(6)
                        plt.plot(bark_axis, N_specific, color=COLORS[0])
                        plt.xlabel("Critical band rate [Bark]")
                        plt.ylabel("N'_zwst [sone/Bark]")
                        plt.title(f"Loudness Zwicker from spectrum - N_zwst = {N:.1f} sone - {wav_name}".format(N))
                        plt.grid()
                        #save
                        plt.savefig(loudness_zwst_spectrum_wav_name, dpi=300)
                        logger.info(f"Loudness Zwicker Spectrum plot saved: {loudness_zwst_spectrum_wav_name}")
                        logger.info("")
                        plt.close()



                    if general_folder == ROUGHNESS_DW_STRING:
                        logger.info("")
                        logger.info("ENTERING THE LOUDNESS_ZWST BLOCK")
                        _, roughness_dw_wav_name = mkdir_folder_wav_name(general_analysis_folder, wav_name, '_roughness_dw.png', 'Roughness')
                        # _, roughness_dw_spectrum_wav_name = mkdir_folder_wav_name(general_analysis_folder, wav_name, '_roughness_dw_spectrum.png', 'Roughness_Spectrum')



                        # ###################################
                        # ###################################
                        # ###################################
                        # # COMPUTTING ROUGHNESS DW
                        # ###################################
                        # ###################################
                        # ###################################
                        logger.info("")
                        logger.info("Computing Roughness DW")
                        r, r_spec, bark, time = roughness_dw(sig, fs, overlap=0)
                        results["metrics"]["roughness_dw"] = {
                            "instantaneous_roughness_asper": r.tolist(),
                            # "specific_roughness_asper_per_bark": r_spec.tolist(),
                            # "bark_axis": bark.tolist(),
                            # "time_axis": time.tolist()
                        }

                        plt.figure(2)
                        plt.plot(time, r, color=COLORS[0])
                        # plt.ylim(0,1.5) # modifying this to plot the whole signal
                        plt.xlabel("Time [s]")
                        plt.ylabel("Roughness [Asper]")
                        plt.title(f'Roughness - {wav_name}')
                        plt.grid()

                        #save
                        plt.savefig(roughness_dw_wav_name, dpi=300)
                        logger.info(f"Roughness plot saved: {roughness_dw_wav_name}")
                        plt.close()



                        ###################################
                        ###################################
                        ###################################
                        # # FROM SPECTRUM
                        ###################################
                        ###################################
                        ######################################################################
                        ###################################
                        ###################################
                        # Compute multiple spectra along time
                        logger.info("")
                        logger.info("Computing Roughness DW from Spectrum")
                        freqs, time, spectrum = stft(sig, fs=fs)

                        # Compute roughness
                        R, R_spec, bark = roughness_dw_freq(spectrum,freqs)
                        results["metrics"]["roughness_dw_from_spectrum"] = {
                            "global_roughness_asper": R,
                            # "specific_roughness_asper_per_bark": R_spec.tolist(),
                            # "bark_axis": bark.tolist()
                        }
                        # logger.info("Roughness_dw = {:.1f} asper".format(R) )
                        # logger.info(f"Roughness_dw spectrum = {R:.1f} asper")
                        # logger.info("Roughness_dw spectrum = {:.1f} asper".format(R) )
                        logger.info(f"Roughness_dw = {R} asper")




                    if general_folder == SHARPNESS_DIN_STRING:
                        logger.info("")
                        logger.info("ENTERING THE SHARPNESS_DIN BLOCK")
                        _, sharpness_din_wav_name = mkdir_folder_wav_name(general_analysis_folder, wav_name, '_sharpness_din.png', 'Sharpness_Din')
                        _, sharpness_din_spectrum_wav_name = mkdir_folder_wav_name(general_analysis_folder, wav_name, '_sharpness_din_spectrum.png', 'Sharpness_Din_Spectrum')



                        # ###################################
                        # ###################################
                        # ###################################
                        # # COMPUTTING ROUGHNESS DW
                        # ###################################
                        # ###################################
                        # ###################################
                        logger.info("")
                        logger.info("Computing Sharpness DIN")



                        for weighting_type in SHARPNESS_DIN_WEITHING:
                            sharpness = sharpness_din_st(sig, fs, weighting=weighting_type)

                            logger.info("Sharpness = {:.1f} acum".format(sharpness) )
                            sharpness_n = "Sharpness = {:.1f} acum".format(sharpness)
                            sharpness, time_axis = sharpness_din_perseg(sig, fs, nperseg=8192 * 2, noverlap=4096, weighting=weighting_type)

                            results["metrics"][f"sharpness_din_{weighting_type}"] = {
                                "global_sharpness_acum": sharpness,
                                # "instantaneous_sharpness_acum": sharpness.tolist(),
                                # "time_axis": time_axis.tolist()
                            }

                            plt.figure(2)
                            plt.plot(time_axis, sharpness, color=COLORS[0])
                            plt.xlabel("Time [s]")
                            plt.ylabel("S_din [acum]")
                            # plt.ylim((0, 3))
                            plt.title(f'Sharpness - {weighting_type} - {sharpness_n} - {wav_name}')
                            plt.grid()

                            # # save
                            plt.savefig(sharpness_din_wav_name, dpi=300)
                            logger.info(f"Sharpness plot saved: {sharpness_din_wav_name}")
                            logger.info("")
                            plt.close()



                        ###################################
                        ###################################
                        ###################################
                        # # FROM SPECTRUM
                        ###################################
                        ###################################
                        ###################################
                        # Compute spectrum
                        logger.info("")
                        logger.info("Computing Sharpness DIN from Spectrum")


                        n = len(sig)
                        spec = np.abs(2 / np.sqrt(2) / n * fft(sig)[0:n//2])
                        freqs = fftfreq(n, 1/fs)[0:n//2]
                        # Compute sharpness
                        S = sharpness_din_freq(spec, freqs)
                        results["metrics"]["sharpness_din_from_spectrum"] = {
                            "global_sharpness_acum": S
                        }
                        logger.info("Sharpness_din = {:.1f} sone".format(S) )

                    


                    ########################################
                    ###################################
                    ###################################
                    #save the json file
                    # with open(json_output_path, 'w') as json_file:
                    #     json.dump(results, json_file, indent=4)

                    # logger.info(f"Metrics saved to JSON: {json_output_path}")

                    with open(json_output_path, 'w', encoding='utf-8') as json_file:
                        json.dump(to_jsonable(results), json_file, indent=4, ensure_ascii=False)

                    logger.info(f"Metrics saved to JSON: {json_output_path}")





if __name__ == "__main__":
    main()