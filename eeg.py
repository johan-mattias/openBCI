import argparse
import time
import brainflow
import numpy as np

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds,BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
from brainflow.exit_codes import *


def main ():
    #BoardShim.enable_board_logger ()
    DataFilter.enable_data_logger ()
    MLModel.enable_ml_logger ()
    '''
    parser = argparse.ArgumentParser ()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument ('--timeout', type = int, help  = 'timeout for device discovery or connection', required = False, default = 0)
    parser.add_argument ('--ip-port', type = int, help  = 'ip port', required = False, default = 0)
    parser.add_argument ('--ip-protocol', type = int, help  = 'ip protocol, check IpProtocolType enum', required = False, default = 0)
    parser.add_argument ('--ip-address', type = str, help  = 'ip address', required = False, default = '')
    parser.add_argument ('--serial-port', type = str, help  = 'serial port', required = False, default = '')
    parser.add_argument ('--mac-address', type = str, help  = 'mac address', required = False, default = '')
    parser.add_argument ('--other-info', type = str, help  = 'other info', required = False, default = '')
    parser.add_argument ('--streamer-params', type = str, help  = 'streamer params', required = False, default = '')
    parser.add_argument ('--serial-number', type = str, help  = 'serial number', required = False, default = '')
    parser.add_argument ('--board-id', type = int, help  = 'board id, check docs to get a list of supported boards', required = True)
    parser.add_argument ('--file', type = str, help  = 'file', required = False, default = '')
    args = parser.parse_args ()

    params = BrainFlowInputParams ()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    
    board = BoardShim (args.board_id, params)
    master_board_id = board.get_board_id ()
    sampling_rate = BoardShim.get_sampling_rate (master_board_id)
    board.prepare_session ()
    board.start_stream (45000, args.streamer_params)
    BoardShim.log_message (LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep (5) # recommended window size for eeg metric calculation is at least 4 seconds, bigger is better
    data = board.get_board_data ()
    board.stop_stream ()
    board.release_session ()
    '''
    print('hello')
    data = DataFilter.read_file ('test.txt')
    print('world')
    master_board_id = 0
    eeg_channels = BoardShim.get_eeg_channels (master_board_id)
    sampling_rate = BoardShim.get_sampling_rate (master_board_id)
    bands = DataFilter.get_avg_band_powers (data, eeg_channels, sampling_rate, True)
    feature_vector = np.concatenate ((bands[0], bands[1]))
    print(feature_vector)

    # calc concentration
    concentration_params = BrainFlowModelParams (BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.KNN.value)
    concentration = MLModel (concentration_params)
    concentration.prepare ()
    print ('Concentration: %f' % concentration.predict (feature_vector))
    concentration.release ()

    # calc relaxation
    relaxation_params = BrainFlowModelParams (BrainFlowMetrics.RELAXATION.value, BrainFlowClassifiers.REGRESSION.value)
    relaxation = MLModel (relaxation_params)
    relaxation.prepare ()
    print ('Relaxation: %f' % relaxation.predict (feature_vector))
    relaxation.release ()

if __name__ == "__main__":
    main ()