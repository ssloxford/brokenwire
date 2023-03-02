import sys
sys.path.append("/home/code/lib/")

from EvaluationUtils import EvaluationUtils
from IPerfEvaluation import IPerfEvaluation
import numpy as np
import argparse
import copy
import glob
import subprocess
import os
from subprocess import Popen
import time
import json

class ConnectionError(Exception):
    pass

def set_noise_level(noise_level):
    # Before setting the noise, make sure that no noise output is currently running
    end_noise_output()
    output_noise = Popen(["sshpass", "-p", "z2b6m0", "ssh", "-oStrictHostKeyChecking=no", "pi@evplctestbed-evcc.lan", "/home/pi/evdisrupt-picoscope-awgn/run.sh", str(noise_level)])
    time.sleep(5)
    output_noise.terminate()

def end_noise_output():
    #sudo pkill -INT python3
    kill_previous_output = Popen(["sshpass", "-p", "z2b6m0", "ssh", "-oStrictHostKeyChecking=no", "pi@evplctestbed-evcc.lan", "sudo", "pkill", "-INT", "python3"])
    # Wait for 5 seconds to give docker enough time to shutdown
    time.sleep(5)
    kill_previous_output.terminate()

def emit_preamble(preamble, lime_sdr_gain):
    run_gnuradio_script = Popen(["python3", "/home/code/scripts/preamble_emission.py", "--preamble", str(preamble), "--lime-sdr-gain", str(lime_sdr_gain)])
    time.sleep(10)
    return run_gnuradio_script

def run_iperf(iperf_evaluation):

    # IPerf Settings
    ip = "192.168.2.1"
    port = "1234"
    evaluation_time = iperf_evaluation.evaluation_time
    bandwidth = "5M"
    
    # Start the IPerf Server
    iperf_server = Popen(["sshpass", "-p", "z2b6m0", "ssh", "-oStrictHostKeyChecking=no", "pi@evplctestbed-secc.lan", "iperf3", "-s", "-p", port, "-J", "-1"], stdout=subprocess.PIPE) 
    # Sleep for a little while to make sure the IPerf Server is up and running
    time.sleep(5)
    
    # Start the IPerf Client
    # Possible error: iperf3: error - unable to connect to server: No route to host
    iperf_client = Popen(["sshpass", "-p", "z2b6m0", "ssh", "-oStrictHostKeyChecking=no", "pi@evplctestbed-evcc.lan", "iperf3", "-u", "-b", bandwidth, "-t", str(evaluation_time), "-p", port, "-c", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        iperf_client.wait(timeout=(evaluation_time + 5))
    except:
        iperf_server.terminate()
        iperf_client.terminate()
        return
    
    iperf_client_output = iperf_client.communicate()[1].decode('utf-8')
    print(iperf_client_output)
    
    if "unable to connect to server" in str(iperf_client_output) or str(iperf_client_output) != "":
        print(f"FAILED: {iperf_client_output}")
        iperf_server.terminate()
        iperf_client.terminate()
        raise ConnectionError('No connection to server possible!')
    
    # Wait for the process, if no client connected kill the process
    iperf_server.wait(timeout=20)
    # Get the output from the IPerf Server Process
    iperf_server_output = iperf_server.communicate()[0].decode('utf-8')
    #print(iperf_server_output)
    
    # Extract the important info from the IPerf Run
    iperf_json_output = json.loads(iperf_server_output)
    try:
        iperf_summary = iperf_json_output["end"]["sum"]
        iperf_evaluation.jitter = iperf_summary["jitter_ms"]
        iperf_evaluation.lost = iperf_summary["lost_packets"]
        iperf_evaluation.sent = iperf_summary["packets"]
        iperf_evaluation.loss = iperf_summary["lost_percent"]
        iperf_evaluation.print_results()
    except:
        pass
    
    # Make sure both processes are terminated
    iperf_server.terminate()
    iperf_client.terminate()

def run_evaluation(number_of_runs, iperf_evaluation):
    noise_levels = [0]
    
    if iperf_evaluation.preamble is None:
        preambles = glob.glob("/home/data/preambles/*.dat")
    else:
        preambles = [iperf_evaluation.preamble]
    
    lime_sdr_min_gain = 12
    lime_sdr_max_gain = 64
    gain_step_size = 2
    
    for preamble in preambles:
    
        # Repeat attack evaluation 
        for run in range(number_of_runs):
            for noise_level in noise_levels:
                #end_noise_output()
                iperf_results = []
                # Count how often the communication was interrupted
                interruption_counter = 0
                
                #if noise_level > 0:
                    #end_noise_output()
                    #set_noise_level(noise_level)
                    # Wait for 15 seconds to make sure the Picoscope has been initilized
                    #time.sleep(15)

                # Iterate from lowest LimeSDR gain to highest
                for lime_sdr_gain in range(lime_sdr_min_gain, lime_sdr_max_gain + 1, gain_step_size):
                    current_evaluation_run = copy.deepcopy(iperf_evaluation)
                    current_evaluation_run.lime_sdr_gain = lime_sdr_gain
                    current_evaluation_run.noise_level = noise_level
                    
                    if interruption_counter > 1:
                        print("Now reached the maximum number of tries")
                        current_evaluation_run.loss = 100
                        iperf_results.append(current_evaluation_run)
                        continue
                        
                    
                    gnuradio_process = emit_preamble(preamble, lime_sdr_gain)
                    time.sleep(4)
                    
                    try:
                        run_iperf(current_evaluation_run)
                    except ConnectionError:
                        print("Catching ConnectionError Exception")
                        current_evaluation_run.loss = 100
                        interruption_counter += 1

                    gnuradio_process.terminate()
                    time.sleep(4)
                    
                    iperf_results.append(current_evaluation_run)

                EvaluationUtils.save_results("results_20211214.csv", iperf_results)
                time.sleep(5)
    #end_noise_output()

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Run evaluation for specific distance.')
    parser.add_argument('--distance', '-d', type=float, help='Distance between PLC and transmitter (m).', required=True)
    parser.add_argument('--amplifier', '-a', type=str, help='Amplifier.', required=False, default="1W")
    parser.add_argument('--voltage', '-v', type=float, help='Amplifier Voltage.', required=False, default=12.0)
    parser.add_argument('--current', '-c', type=float, help='Amplifier Current.', required=False, default=0.31)
    parser.add_argument('--preamble', '-p', type=str, help='Path to the preamble.', required=False)
    parser.add_argument('--time', '-t', type=int, help='Attack duration in seconds.', required=False, default=30)
    parser.add_argument('--cable_length', type=int, help='Length of the charging cable (m).', required=False, default=4)
    parser.add_argument('--angle', type=int, help='Angle between attacker and charging cable.', required=False, default=0)
    parser.add_argument('--antenna_position', type=str, help='Description of antenna position.', required=False, default="Nearly centered, parallel")
    parser.add_argument('--antenna', type=str, help='Description of antenna setting.', required=False, default="One dipole unrolled, one rolled")
    parser.add_argument('--number_of_runs', '-r', type=int, help='Number of runs.', required=False, default=1)
    args = parser.parse_args()
    
    iperf_evaluation = IPerfEvaluation(args.distance, args.amplifier, args.voltage, args.current, args.preamble, args.time, args.cable_length, args.angle, args.antenna_position, args.antenna)
    
    run_evaluation(args.number_of_runs, iperf_evaluation)
