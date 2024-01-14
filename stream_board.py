import time
import brainflow
import numpy as np
from midiutil import MIDIFile

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowOperations, DetrendOperations, NoiseTypes

import serial
import random

arduino = serial.Serial(port='/dev/cu.usbmodem101', baudrate=115200, timeout=2)


def main():
    params = BrainFlowInputParams()
    params.ip_port=6789
    board_id = BoardIds.CYTON_WIFI_BOARD.value
    board = BoardShim(board_id, params)
    eeg_channels = board.get_eeg_channels(board_id)
    sampling_rate = board.get_sampling_rate(board_id)
    timestamp = BoardShim.get_timestamp_channel(board_id)

    board = BoardShim(board_id, params)
    board.prepare_session()

    board.start_stream()
    
    increases = 0
    decreases = 0
    lastnum = 0
    n = 0
    threshhold = 4

    for _ in range(100):
    
        BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
        time.sleep(2)
        nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
        data = board.get_board_data()
        eeg_channels = BoardShim.get_eeg_channels(board_id)
        
            
        eeg_channel = eeg_channels[3]
        psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate, WindowOperations.NO_WINDOW.value)
        df = pd.DataFrame(np.transpose(data))
        plt.figure()
        df[eeg_channels[:3]].plot(subplots=True)
        plt.savefig("before_processing.png")

        # for demo apply different filters to different channels, in production choose one
        for count, channel in enumerate(eeg_channels):
            # # filters work in-place
            DataFilter.perform_bandpass(data[channel], BoardShim.get_sampling_rate(board_id), 1, 30, 4,
                                            FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.remove_environmental_noise(data[channel], BoardShim.get_sampling_rate(board_id), NoiseTypes.FIFTY.value)
        
        bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)

        df = pd.DataFrame(np.transpose(data))
        plt.figure()
        df[eeg_channels[:3]].plot(subplots=True)
        plt.savefig("after_processing.png")

        cycled_data = []
        for i in enumerate(data[eeg_channels[0]]):
            if i[0] % 50 == 0:
                cycled_data.append(i[1])

        print("Cycling through data...")
        musical_notes = []
        # Yes... it's really just a bunch of if statments 😅
        
        tot = 0
        nums = 0

        print("-----")
        
        for i in cycled_data:

            tot += i
            nums += 1

            

            # if i < 1 and i > 0:
            #     musical_notes.append(60)
            #     print(1)
            # if i < 0 and i > -1:
            #     musical_notes.append(59)
            #     print(2)
            # if i < -1 and i > -2:
            #     musical_notes.append(58)
            #     print(3)
            # if i < -2:
            #     musical_notes.append(57)
            #     print(4)
            # if i > 1 and i < 2:
            #     musical_notes.append(62)
            #     print(5)
            # if i > 2 and i < 3:
            #     musical_notes.append(63)
            #     print(6)
            # if i > 3 and i < 4:
            #     musical_notes.append(64)
            #     print(7)
            # if i > 4 and i < 5:
            #     musical_notes.append(65)
            #     print(8)
            # if i > 5:
            #     musical_notes.append(66)
            #     print(9)

        tot = abs(tot/nums)
        print(tot)

        if tot > lastnum:
            increases+=1
            decreases-=1
        elif tot < lastnum:
            decreases+=1
            increases-=1
        increases = max(-5, increases) 
        decreases = max(-5, decreases) 

        lastnum = tot
        
        if increases >= threshhold:
            n+=1
            increases = 0
            decreases = 0
        elif decreases >= threshhold:
            n-=1
            increases = 0
            decreases = 0

        n = max(0, min(3, n)) 

        # if tot < 1000:
        #     n = 0
        # elif 100 < tot < 1500:
        #     n = 1
        # else:
        #     n = 2
        
        print(n)
        
        # n = random.randint(0, 2)
        # print(n)

        arduino.write(bytes(str(n), 'utf-8'))

    # print("Converting data into music notes")

    # track     = 0
    # channel   = 0
    # time_beat = 0   # In beats
    # duration  = 1   # In beats
    # tempo     = 250  # In BPM
    # volume    = 100 # 0-127, as per the MIDI standard

    # MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track automatically created)
    # MyMIDI.addTempo(track,time_beat, tempo)

    # for pitch in musical_notes:
    #     MyMIDI.addNote(track, channel, pitch, time_beat, duration, volume)
    #     time_beat = time_beat + 1

    # with open("le-music.mid", "wb") as output_file:
    #     MyMIDI.writeFile(output_file)

    
    # print("Conversion completed, play file le-music.mid")

if __name__ == "__main__":
    main()