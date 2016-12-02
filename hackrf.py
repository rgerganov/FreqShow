import os
import subprocess
import numpy as np

HACKRF_FILE = '/home/pi/hackrf-recording.cs8'
class HackRf(object):

    def __init__(self):
        self.p = None
	self.rec_dest = "/dev/null"
	self.shm = open("/dev/shm/hackrf", "rb", 0)
	self.rnd = open("/dev/urandom", "rb")

	#self.center = 40000000
	#self.rate = 2000000
	self.mode = "-r"
	#self.start_process()

    def start_process(self):
        if self.mode == '-t':
            hf_file = HACKRF_FILE
        else:
            hf_file = self.rec_dest
        args = ['/usr/local/bin/hackrf_transfer',
                                   '-f',
                                   str(self.center),
                                   '-s',
                                   str(self.rate),
                                   self.mode,
                                   hf_file]
        if self.mode == '-t':
            args.extend('-a 1 -x 47'.split())
        self.p = subprocess.Popen(args)

    def stop_process(self):
        self.p.kill()
	self.p.wait()

    def read_samples(self, num_samples):
	self.shm.seek(0)
        raw_data = self.shm.read(num_samples * 2)

	if len(raw_data) < (num_samples * 2):
		raw_data = self.rnd.read(num_samples * 2)
        #
        #if len(raw_data) < num_samples*2:
        #    raise Exception('fira!!!!')

        iq = self.packed_bytes_to_iq(bytearray(raw_data))
        return iq

    def packed_bytes_to_iq(self, bytes):
        ''' Convenience function to unpack array of bytes to Python list/array
        of complex numbers and normalize range. Called automatically by read_samples()
        '''
        # use NumPy array
        iq = np.empty(len(bytes)//2, 'complex')
        iq.real, iq.imag = bytes[::2], bytes[1::2]
        iq /= (255/2)
        iq -= (1 + 1j)
        return iq

    def get_center_freq(self):
        return self.center

    def set_center_freq(self, freq):
	self.center = freq

    def get_sample_rate(self):
        return self.rate

    def set_sample_rate(self, rate):
	self.rate = rate

    def get_gain(self):
        return 10

    def set_manual_gain_enabled(self, flag):
        pass

    def set_gain(self, gain):
        pass

    def get_record_destination(self):
	return self.rec_dest

    def set_record_destination(self, dest):
	self.rec_dest = dest

