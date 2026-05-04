import numpy as np
from ekg_testbench import EKGTestBench
from scipy.signal import find_peaks

def detect_heartbeats(filepath):
    """
    Perform analysis to detect location of heartbeats
    :param filepath: A valid path to a CSV file of heart beats
    :return: signal: a signal that will be plotted
    beats: the indices of detected heartbeats
    """
    if filepath == '':
        return list()

    # import the CSV file using numpy
    path = filepath

    # load data in matrix from CSV file; skip first two rows
    ## your code here
    data = np.loadtxt(path, delimiter=',', skiprows=2)

    # save each vector as own variable
    ## your code here
    ##seperate data into columns
    time = data[:, 0]
    mlii = data[:, 1]
    v5 = data[:, 2]

    # identify one column to process. Call that column signal
    ##mlii col selected

    signal = mlii ## your code here

    # pass data through LOW PASS FILTER (OPTIONAL)
    ## your code here
    ##length of win
    low_pass_window = 2
    ##creation of averaging filter
    low_pass_kernel = np.ones(low_pass_window) / low_pass_window
    ##applying filter and keep length
    low_pass = np.convolve(signal, low_pass_kernel, mode='same')

    # pass data through HIGH PASS FILTER (OPTIONAL) to create BAND PASS result
    ## your code here

    ##length of window
    high_pass_window = 77
    ##creation of avg filter
    baseline_kernel = np.ones(high_pass_window) / high_pass_window
    ##applying filter and keep length
    baseline = np.convolve(low_pass, baseline_kernel, mode='same')
    ##apply bandpass using lowpass and baseline trends
    band_pass = low_pass - baseline

    # pass data through differentiator
    ## your code here
    ##diff and keep length
    diff = np.diff(band_pass, prepend=band_pass[0])

    # pass data through square function
    ## your code here
    squared = diff * diff

    # pass through moving average window
    ## your code here
    #find sample rate from time data
    sample_rate = 1.0 / np.mean(np.diff(time))
    ##use sample to create 80ms window
    moving_average_window = int(0.042 * sample_rate)
    ##create ma avg filter
    ma_kernel = np.ones(moving_average_window) / moving_average_window
    ##apply filter to squared data
    signal = np.convolve(squared, ma_kernel, mode='same')

    # use find_peaks to identify peaks within averaged/filtered data
    # save the peaks result and return as part of testbench result

    ## your code here peaks,_ = find_peaks(....)
    ##make min dist win between beats
    minimum_distance = int(0.21 * sample_rate)
    #set min peak based on avg lvl and std variations
    peak_height = np.mean(signal) + 0.085 * np.std(signal)

    ##detect peaks based on all requirments
    peaks, _ = find_peaks(signal, height=peak_height, distance=minimum_distance)

    beats = peaks

    # do not modify this line
    return signal, beats


# when running this file directly, this will execute first
if __name__ == "__main__":

    # place here so doesn't cause import error
    import matplotlib.pyplot as plt

    # database name
    database_name = 'mitdb_201'

    # set to true if you wish to generate a debug file
    file_debug = False

    # set to true if you wish to print overall stats to the screen
    print_debug = True

    # set to true if you wish to show a plot of each detection process
    show_plot = False

    ### DO NOT MODIFY BELOW THIS LINE!!! ###

    # path to ekg folder
    path_to_folder = "../../../data/ekg/"

    # select a signal file to run
    signal_filepath = path_to_folder + database_name + ".csv"

    # call main() and run against the file. Should return the filtered
    # signal and identified peaks
    (signal, peaks) = detect_heartbeats(signal_filepath)

    # matched is a list of (peak, annotation) pairs; unmatched is a list of peaks that were
    # not matched to any annotation; and remaining is annotations that were not matched.
    annotation_path = path_to_folder + database_name + "_annotations.txt"
    tb = EKGTestBench(annotation_path)
    peaks_list = peaks.tolist()
    (matched, unmatched, remaining) = tb.generate_stats(peaks_list)

    # if was matched, then is true positive
    true_positive = len(matched)

    # if response was unmatched, then is false positive
    false_positive = len(unmatched)

    # whatever remains in annotations is a missed detection
    false_negative = len(remaining)

    # calculate f1 score
    f1 = true_positive / (true_positive + 0.5 * (false_positive + false_negative))

    # if we wish to show the resulting plot
    if show_plot:
        # make a nice plt of results
        plt.title('Signal for ' + database_name + " with detections")

        plt.plot(signal, label="Filtered Signal")
        plt.plot(peaks, signal[peaks], 'p', label='Detected Peaks')

        true_annotations = np.asarray(tb.annotation_indices)
        plt.plot(true_annotations, signal[true_annotations], 'o', label='True Annotations')

        plt.legend()

        # uncomment line to show the plot
        plt.show()

    # if we wish to save all the stats to a file
    if file_debug:
        # print out more complex stats to the debug file
        debug_file_path = database_name + "_debug_stats.txt"
        debug_file = open(debug_file_path, 'w')

        # print out indices of all false positives
        debug_file.writelines("-----False Positives Indices-----\n")
        for fp in unmatched:
            debug_file.writelines(str(fp) + "\n")

        # print out indices of all false negatives
        debug_file.writelines("-----False Negatives Indices-----\n")
        for fn in remaining:
            debug_file.writelines(str(fn.sample) + "\n")

        # close file that we writing
        debug_file.close()

    if print_debug:
        print("-------------------------------------------------")
        print("Database|\t\tTP|\t\tFP|\t\tFN|\t\tF1")
        print(database_name, "|\t\t", true_positive, "|\t", false_positive, '|\t', false_negative, '|\t', round(f1, 3))
        print("-------------------------------------------------")

    print("Done!")
