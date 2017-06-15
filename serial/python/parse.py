import exceptions

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines 

from time import sleep
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread

from packet import *

class Parse(QThread):
    def __init__(self, dev_type='elka', q=None):
        QThread.__init__(self)
        self.dev_type = dev_type
        self.q = q

    # Returns updated `data` variable
    def parse_packet(self, pkts=None, pkt_type='elka'):
        # Elka packet has max 32B as follows:
        #   1B length (not including this byte)
        #   3B packet type
        #   0-28B data
        #       Each data value is 2B for up to 14 data values
        if pkt_type == 'elka':
            return self.parse_elka_packet(pkts=pkts)
        if pkt_type == 'legacy_elka':
            return self.parse_legacy_elka_packet(pkts=pkts)
        elif pkt_type == 'spektrum':
            return self.parse_spektrum_packet(pkts=pkts)
        else:
            raise exceptions.PacketTypeException('packet type {0} does not exist'
                                      .format(pkt_type))

    def parse_elka_packet(self, pkts=None):
        if not pkts.has_key('elka_data') or pkts['elka_data'] is None:
            idx = 0
        else:
            idx = pkts['elka_data'].shape[0]


    #FIXME hardcodes length and ignores packet type
    def parse_legacy_elka_packet(self, pkts=None):
        # idx is equal to number of rows in 2d data array 
        if pkts['legacy_elka_data'] is None:
            idx = 0
        else:
            idx = pkts['legacy_elka_data'].shape[0]

        # Make sure queue is populated with data
        # and that the next bytes are data
        if len(self.q) > 1 and\
           int(self.q.popleft().encode('hex'),16) == 255 and\
           int(self.q.popleft().encode('hex'),16) == 255:
            pkt_data = np.array([idx],dtype=np.int16)
            while len(self.q) < 8:
                sleep(.01)

            for i in range(LegacyElkaPacket.DATA_LENGTH):
                pkt_data = np.append(pkt_data,
                        (int(self.q.popleft().encode('hex'),16) << 8 |\
                         int(self.q.popleft().encode('hex'),16)))
            
            if pkts['elka_data'] is None:
                pkts['elka_data'] = np.array([pkt_data])
            else:
                if np.all(np.less_equal(pkt_data[1:],2000)) and\
                   np.all(np.greater_equal(pkt_data[1:],1000)):
                    print pkt_data
                    np.contatenate((pkts['elka_data'],[pkt_data]),axis=0)

    #FIXME Ensure that byte ordering is correct!!!
    #      It was incorrect for `values` array
    def parse_spektrum_packet(self, pkts=None):
        print 'here'
        if len(self.q) >= SpektrumPacket.element_lengths['header'] and\
           ord(self.q.popleft()) == 255 and\
           ord(self.q.popleft()) == 0 and\
           ord(self.q.popleft()) == 255 and\
           ord(self.q.popleft()) == 0:

            pkt_len = SpektrumPacket.PACKET_LENGTH-\
                      SpektrumPacket.element_lengths['header']
            while len(self.q) < pkt_len:
                sleep(.01)

            # Pop everything off
            # Multi-byte elements that must be conjoined are packed
            # LSB first
            np.append(pkts['timestamp_last_signal'],
                np.uint64(ord(self.q.popleft()) |\
                          (ord(self.q.popleft()) << 8) |\
                          (ord(self.q.popleft()) << 16) |\
                          (ord(self.q.popleft()) << 24) |\
                          (ord(self.q.popleft()) << 32) |\
                          (ord(self.q.popleft()) << 40) |\
                          (ord(self.q.popleft()) << 48) |\
                          (ord(self.q.popleft()) << 56)))

            channel_count = ord(self.q.popleft()) |\
                            (ord(self.q.popleft()) << 8) |\
                            (ord(self.q.popleft()) << 16) |\
                            (ord(self.q.popleft()) << 24)
            np.append(pkts['timestamp_last_signal'],
                np.uint32(channel_count))

            np.append(pkts['rssi'],
                np.int32(ord(self.q.popleft()) |\
                          (ord(self.q.popleft()) << 8) |\
                          (ord(self.q.popleft()) << 16) |\
                          (ord(self.q.popleft()) << 24)))

            np.append(pkts['rc_failsafe'],
                np.bool(ord(self.q.popleft())))

            np.append(pkts['rc_lost'],
                np.bool(ord(self.q.popleft())))

            np.append(pkts['rc_lost_frame_count'],
                np.uint16(ord(self.q.popleft()) |
                          (ord(self.q.popleft()) << 8)))

            np.append(pkts['rc_total_frame_count'],
                np.uint16(ord(self.q.popleft()) |
                          (ord(self.q.popleft()) << 8)))

            np.append(pkts['rc_ppm_frame_length'],
                np.uint16(ord(self.q.popleft()) |
                          (ord(self.q.popleft()) << 8)))

            np.append(pkts['input_source'],
                np.uint8(ord(self.q.popleft())))

            # values
            # idx is equal to number of rows in 2d data array 
            if pkts['spektrum_values'] is None:
                idx = 0
            else:
                idx = pkts['spektrum_values'].shape[0]

            pkt_data = np.array([idx],dtype=np.int16)

            for i in range(SpektrumPacket.MAX_CHANNELS):
                if i < channel_count:
                    pkt_data = np.append(pkt_data,
                        np.uint16((ord(self.q.popleft()) << 8)|\
                                  ord(self.q.popleft())))
                else:
                    pkt_data = np.append(pkt_data,0)
            print idx, channel_count
            print pkts['spektrum_values']
            
            pkts['spektrum_values'] =\
                np.concatenate((pkts['spektrum_values'],[pkt_data]),axis=0)

    #FIXME get rid of this. legacy
    def plot_data(self,ax=None,data=None,dtype='elka'):
        if data is not None and ax is not None:
            if dtype is 'elka':
                ax.plot(data[:,0],data[:,1],'r--',
                        data[:,0],data[:,2],'b--',
                        data[:,0],data[:,3],'k--',
                        data[:,0],data[:,4],'g--')
            elif dtype is 'spektrum':
                ax.plot(data[:,0],data[:,1],'r--',
                        data[:,0],data[:,2],'b--',
                        data[:,0],data[:,3],'k--',
                        data[:,0],data[:,4],'g--')

    def run(self):
        ''' Initialize pkts dict to contain initial zero packet '''
        pkts=\
            {'legacy_elka_data':
                    np.zeros((1,LegacyElkaPacket.DATA_LENGTH),dtype=np.uint16), 'timestamp_last_signal':
                    np.zeros(1,dtype=np.uint64),
              'channel_count':
                    np.zeros(1,dtype=np.uint32),
              'rssi':
                    np.zeros(1,dtype=np.int32),
              'rc_failsafe':
                    np.zeros(1,dtype=np.bool),
              'rc_lost':
                    np.zeros(1,dtype=np.bool),
              'rc_lost_frame_count':
                    np.zeros(1,dtype=np.uint16),
              'rc_total_frame_count':
                    np.zeros(1,dtype=np.uint16),
              'rc_ppm_frame_length':
                    np.zeros(1,dtype=np.uint16),
              'input_source':
                    np.zeros(1,dtype=np.uint8),
              'spektrum_values': np.zeros((1,SpektrumPacket.MAX_CHANNELS+1),dtype=np.uint16)
            }

        '''
        fig,ax = plt.subplots()

        plot = True
        '''

        while not self.exiting:
            if len(self.q) == 0:
                sleep(.01)
            else:
                '''
                parse_packet(q=q,pkts=pkts,pkt_type='elka')
                if pkts['elka_data'] is not None:
                    plot_data(ax=ax,data=pkts['elka_data'],dtype='elka')
                    plt.pause(0.001)
                parse_packet(pkts=pkts,pkt_type='spektrum')
                if pkts['spektrum_values'].shape[0] > 2000 and plot:
                    plot = False
                    plot_data(ax=ax,data=pkts['spektrum_values'],
                              dtype='spektrum')
                    plt.show()
                '''
                self.parse_packet(pkts=pkts,pkt_type='elka')

    def __del__(self):
        self.exiting=True
        self.wait()

