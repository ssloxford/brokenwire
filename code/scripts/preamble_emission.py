#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.9.2.0

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
from gnuradio import soapy




class preamble_emission(gr.top_block):

    def __init__(self, preamble='/home/data/preambles/captured_preamble.dat', lime_sdr_gain=-12):
        gr.top_block.__init__(self, "Brokenwire", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.preamble = preamble
        self.lime_sdr_gain = lime_sdr_gain

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 25e6
        self.freq = freq = 17e6

        ##################################################
        # Blocks
        ##################################################
        self.soapy_limesdr_sink_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_sink_0.set_bandwidth(0, 0.0)
        self.soapy_limesdr_sink_0.set_frequency(0, freq)
        self.soapy_limesdr_sink_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_sink_0.set_gain(0, min(max(lime_sdr_gain, -12.0), 64.0))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, preamble, True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.soapy_limesdr_sink_0, 0))


    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.blocks_file_source_0.open(self.preamble, True)

    def get_lime_sdr_gain(self):
        return self.lime_sdr_gain

    def set_lime_sdr_gain(self, lime_sdr_gain):
        self.lime_sdr_gain = lime_sdr_gain
        self.soapy_limesdr_sink_0.set_gain(0, min(max(self.lime_sdr_gain, -12.0), 64.0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.soapy_limesdr_sink_0.set_sample_rate(0, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_limesdr_sink_0.set_frequency(0, self.freq)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--preamble", dest="preamble", type=str, default='/home/data/preambles/captured_preamble.dat',
        help="Set Preamble [default=%(default)r]")
    parser.add_argument(
        "--lime-sdr-gain", dest="lime_sdr_gain", type=intx, default=-12,
        help="Set LimeSDR Gain [default=%(default)r]")
    return parser


def main(top_block_cls=preamble_emission, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(preamble=options.preamble, lime_sdr_gain=options.lime_sdr_gain)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

#    try:
#        input('Press Enter to quit: ')
#    except EOFError:
#        pass
    #tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
