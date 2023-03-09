#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Brokenwire Osmocom
# Author: FlUxIuS (Penthertz)
# GNU Radio version: 3.10.5.1

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time




class brokenwireosmo(gr.top_block):

    def __init__(self, devicestring="", inputfile='captured_preamble.dat', txgain=10, var_freq=int(17e6)):
        gr.top_block.__init__(self, "Brokenwire Osmocom", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.devicestring = devicestring
        self.inputfile = inputfile
        self.txgain = txgain
        self.var_freq = var_freq

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 25e6
        self.freq = freq = var_freq

        ##################################################
        # Blocks
        ##################################################

        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + devicestring
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(txgain, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, inputfile, True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.osmosdr_sink_0, 0))


    def get_devicestring(self):
        return self.devicestring

    def set_devicestring(self, devicestring):
        self.devicestring = devicestring

    def get_inputfile(self):
        return self.inputfile

    def set_inputfile(self, inputfile):
        self.inputfile = inputfile
        self.blocks_file_source_0.open(self.inputfile, True)

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.osmosdr_sink_0.set_gain(self.txgain, 0)

    def get_var_freq(self):
        return self.var_freq

    def set_var_freq(self, var_freq):
        self.var_freq = var_freq
        self.set_freq(self.var_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--devicestring", dest="devicestring", type=str, default="",
        help="Set deviceargs [default=%(default)r]")
    parser.add_argument(
        "--inputfile", dest="inputfile", type=str, default='captured_preamble.dat',
        help="Set preamblefile [default=%(default)r]")
    parser.add_argument(
        "--txgain", dest="txgain", type=intx, default=10,
        help="Set txgain [default=%(default)r]")
    parser.add_argument(
        "--var-freq", dest="var_freq", type=intx, default=int(17e6),
        help="Set frequency [default=%(default)r]")
    return parser


def main(top_block_cls=brokenwireosmo, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(devicestring=options.devicestring, inputfile=options.inputfile, txgain=options.txgain, var_freq=options.var_freq)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
