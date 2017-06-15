class SpektrumPacket(object):
    MAX_CHANNELS = 18
    CHANNEL_VALUE_LENGTH = 2
    element_lengths =\
        { 'header':4,
          'timestamp_last_signal':8,
          'channel_count':4,
          'rssi':4,
          'rc_failsafe':1,
          'rc_lost':1,
          'rc_lost_frame_count':2,
          'rc_total_frame_count':2,
          'rc_ppm_frame_length':2,
          'input_source':1,
          'values':2 }
    PACKET_LENGTH = sum(element_lengths.values()) -\
                        element_lengths['values'] +\
                        element_lengths['values']*MAX_CHANNELS

class LegacyElkaPacket(object):
    DATA_LENGTH = 4 

class ElkaPacket(object):
    MAX_LENGTH = 261
