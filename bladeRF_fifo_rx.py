#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: bladeRF FIFO RX
# Author: Jon Szymaniak <jon.szymaniak@nuand.com>
# Description: RX bladeRF SC16 Q11 samples from a FIFO, convert them to GR Complex values, and write them to a GUI sink.
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from gnuradio import qtgui

class bladeRF_fifo_rx(gr.top_block, Qt.QWidget):

    def __init__(self, fifo='/home/dionisiocar/sdr/receiver_generator/rx_samples.bin', frequency=100e6, sample_rate=8000000):
        gr.top_block.__init__(self, "bladeRF FIFO RX")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("bladeRF FIFO RX")
        qtgui.util.check_set_qss()
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

        self.settings = Qt.QSettings("GNU Radio", "bladeRF_fifo_rx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.fifo = fifo
        self.frequency = frequency
        self.sample_rate = sample_rate

        ##################################################
        # Variables
        ##################################################
        self.sample_rate_range = sample_rate_range = sample_rate
        self.frequency_range = frequency_range = frequency

        ##################################################
        # Blocks
        ##################################################
        self._sample_rate_range_range = Range(160e3, 40e6, 1e6, sample_rate, 200)
        self._sample_rate_range_win = RangeWidget(self._sample_rate_range_range, self.set_sample_rate_range, 'Sample Rate', "counter", float)
        self.top_grid_layout.addWidget(self._sample_rate_range_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._frequency_range_range = Range(100e6, 500e6, 1e6, frequency, 200)
        self._frequency_range_win = RangeWidget(self._frequency_range_range, self.set_frequency_range, 'Frequency', "counter", float)
        self.top_grid_layout.addWidget(self._frequency_range_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            frequency_range, #fc
            sample_rate_range, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 1, 0, 1, 8)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc((1.0 / 2048.0))
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(True, False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*2, fifo, False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "bladeRF_fifo_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_fifo(self):
        return self.fifo

    def set_fifo(self, fifo):
        self.fifo = fifo
        self.blocks_file_source_0.open(self.fifo, False)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.set_frequency_range(self.frequency)

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.set_sample_rate_range(self.sample_rate)

    def get_sample_rate_range(self):
        return self.sample_rate_range

    def set_sample_rate_range(self, sample_rate_range):
        self.sample_rate_range = sample_rate_range
        self.qtgui_sink_x_0.set_frequency_range(self.frequency_range, self.sample_rate_range)

    def get_frequency_range(self):
        return self.frequency_range

    def set_frequency_range(self, frequency_range):
        self.frequency_range = frequency_range
        self.qtgui_sink_x_0.set_frequency_range(self.frequency_range, self.sample_rate_range)


def argument_parser():
    description = 'RX bladeRF SC16 Q11 samples from a FIFO, convert them to GR Complex values, and write them to a GUI sink.'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-f", "--fifo", dest="fifo", type=str, default='/home/dionisiocar/sdr/receiver_generator/rx_samples.bin',
        help="Set Full path to FIFO [default=%(default)r]")
    parser.add_argument(
        "--frequency", dest="frequency", type=eng_float, default="100.0M",
        help="Set Frequency [default=%(default)r]")
    parser.add_argument(
        "-s", "--sample-rate", dest="sample_rate", type=eng_float, default="8.0M",
        help="Set Sample Rate [default=%(default)r]")
    return parser


def main(top_block_cls=bladeRF_fifo_rx, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(fifo=options.fifo, frequency=options.frequency, sample_rate=options.sample_rate)
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
