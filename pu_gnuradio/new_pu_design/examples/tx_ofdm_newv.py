#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: OFDM PU Phy
# Generated: Fri Feb 17 23:48:32 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import dbconnect
import sys
import time
import arg_parser

# create the object that will have the config
pu_params = arg_parser.Params()
pu_params.parse_arguments("tx_ofdm_newv")

class tx_ofdm_newv(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM PU Phy")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("OFDM PU Phy")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "tx_ofdm_newv")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6
        self.taps = taps = filter.firdes.low_pass(1,samp_rate, 0.98e6,0.5e6)
        self.sync_word2 = sync_word2 = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
        self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
        self.packet_len = packet_len = 64
        self.occupied_carriers = occupied_carriers = (range(-26, -21) + range(-20, -7) + range(-6, 0) + range(1, 7) + range(8, 21) + range(22, 27),)
        self.len_tag_key = len_tag_key = "packet_len"
        self.interp_factor = interp_factor = 5
        self.fft_len = fft_len = 64
        self.decim_factor = decim_factor = 1

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	"",#",".join(("addr=192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(pu_params.frequency, 0)
        self.uhd_usrp_sink_0.set_gain(15, 0)
        self.uhd_usrp_sink_0.set_antenna(pu_params.antenna, 0)
        self.rational_resampler_xxx_0_0_1_1 = filter.rational_resampler_ccc(
                interpolation=interp_factor,
                decimation=decim_factor,
                taps=(taps),
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0_1_0 = filter.rational_resampler_ccc(
                interpolation=interp_factor,
                decimation=decim_factor,
                taps=(taps),
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0_1 = filter.rational_resampler_ccc(
                interpolation=interp_factor,
                decimation=decim_factor,
                taps=(taps),
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=interp_factor,
                decimation=decim_factor,
                taps=(taps),
                fractional_bw=None,
        )
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
        	  fft_len=fft_len, cp_len=fft_len/4,
        	  packet_length_tag_key=len_tag_key,
        	  occupied_carriers=occupied_carriers,
        	  pilot_carriers=pilot_carriers,
        	  pilot_symbols=pilot_symbols,
        	  sync_word1=sync_word1,
        	  sync_word2=sync_word2,
        	  bps_header=1,
        	  bps_payload=2,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )

        self.dbconnect_packet_controller_0 = dbconnect.packet_controller(samp_rate/interp_factor, (10000,), 5, 10, 2, 20, 10, 5, 6643, \
        pu_params.gain_period, pu_params.gain, pu_params.scenario, True, pu_params.channel1, pu_params.channel2)
        self.dbconnect_cmd_pktgen_0 = dbconnect.cmd_pktgen(pu_params.db_ip, 5003, 64, True)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.complex_t, "packet_len")
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        self.blocks_multiply_xx_0_3 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_2 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.09, ))
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_add_xx_2 = blocks.add_vcc(1)
        self.analog_sig_source_x_0_3 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -3.75e6, 1, 0)
        self.analog_sig_source_x_0_2 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 3.75e6, 1, 0)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -1.25e6, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1.25e6, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.dbconnect_packet_controller_0, 'in0'))
        self.msg_connect((self.dbconnect_cmd_pktgen_0, 'out0'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.dbconnect_packet_controller_0, 'gcmd'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.dbconnect_packet_controller_0, 'cmd'), (self.dbconnect_cmd_pktgen_0, 'cmd'))

        # added new gain
        self.msg_connect((self.dbconnect_packet_controller_0, 'gcmd'), (self.uhd_usrp_sink_0, 'command'))

        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_multiply_xx_0_2, 1))
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_multiply_xx_0_3, 1))
        self.connect((self.blocks_add_xx_2, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_2, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.blocks_add_xx_2, 1))
        self.connect((self.blocks_multiply_xx_0_2, 0), (self.blocks_add_xx_2, 2))
        self.connect((self.blocks_multiply_xx_0_3, 0), (self.blocks_add_xx_2, 3))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))
        self.connect((self.dbconnect_packet_controller_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.dbconnect_packet_controller_0, 1), (self.rational_resampler_xxx_0_0_1, 0))
        self.connect((self.dbconnect_packet_controller_0, 2), (self.rational_resampler_xxx_0_0_1_0, 0))
        self.connect((self.dbconnect_packet_controller_0, 3), (self.rational_resampler_xxx_0_0_1_1, 0))
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_1, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.rational_resampler_xxx_0_0_1_0, 0), (self.blocks_multiply_xx_0_2, 0))
        self.connect((self.rational_resampler_xxx_0_0_1_1, 0), (self.blocks_multiply_xx_0_3, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx_ofdm_newv")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_taps(filter.firdes.low_pass(1,self.samp_rate, 0.98e6,0.5e6))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.analog_sig_source_x_0_3.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_2.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.rational_resampler_xxx_0_0_1_1.set_taps((self.taps))
        self.rational_resampler_xxx_0_0_1_0.set_taps((self.taps))
        self.rational_resampler_xxx_0_0_1.set_taps((self.taps))
        self.rational_resampler_xxx_0_0.set_taps((self.taps))

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key

    def get_interp_factor(self):
        return self.interp_factor

    def set_interp_factor(self, interp_factor):
        self.interp_factor = interp_factor

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len

    def get_decim_factor(self):
        return self.decim_factor

    def set_decim_factor(self, decim_factor):
        self.decim_factor = decim_factor


def main(top_block_cls=tx_ofdm_newv, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
