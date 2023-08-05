"""
OsensaIMOS: A Python module for interfacing with OSENSA IMOS

Created on Fri Nov 24 16:28:12 2017

@author: Sharada Balaji, Caleb Ng
"""

__author__   = 'Sharada Balaji, Caleb Ng'
__url__      = 'https://github.com/osensa/osensaimos'
__license__  = 'MIT License'

__version__  = '0.2.4'
__status__   = 'Beta'

import sys
import glob
import serial
import json
import time
import collections
from struct import pack, unpack, calcsize
from .minimalmodbusosensa import Instrument, SecurityError
from math import sqrt
import numpy as np

#5 second timeout for some commands
class TimeoutError(Exception):
    def __init__(self, value = "Timed out"):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    

class InvalidSetupError(Exception):
    pass

"""
DEFAULT SETTINGS:
    baudrate            = 9600
    # of databits       = 8
    parity              = NONE
    stop bits           = 1
"""
SLAVEADDRESS = 1
BAUDRATE = 115200
NUMBITS = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOP = serial.STOPBITS_ONE
PY3K = sys.version_info >= (3, 0)

def serial_get_portlist():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    portlist = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            portlist.append(port)
            print(port)
        except (OSError, serial.SerialException):
            pass
    return portlist


#convert binary data file to a formatted CSV file
def convert_binary_file(binary_filename, output_filename, parameter_list, stream_rate):
    """Convert data from a binary data file into a formatted CSV file.

    Args:
        * binary_filename (string): Name/path of binary data file
        * output_filename (string): Name/path of output CSV file 
        * parameter_list (list of strings): List of parameters that were streamed. While the actual names of these values don't matter, it is important to sure the number of parameters matches the streamed parameters otherwise the CRC will not match.
        * stream_rate (integer): Frequency at which to stream data at (100Hz, 200Hz, 400Hz, 800Hz)

    """
    # Check file parameters
    if (binary_filename is None or binary_filename.strip().isspace()):
        raise ValueError('Binary input file name cannot be empty')
    if (output_filename is None or output_filename.strip().isspace()):
        raise ValueError('Output file name cannot be empty')
    if (not output_filename.endswith('.csv')):
        output_filename += '.csv'
    # Check parameter list
    if (parameter_list is None or len(parameter_list) < 1):
        raise ValueError('Parameter list cannot be empty')
    # Check stream rate value
    if stream_rate != 100 and stream_rate != 200 and stream_rate != 400 and stream_rate != 800:
        raise ValueError('{} is not a supported stream rate'.format(stream_rate))
    # Open files
    infile = open(binary_filename, 'rb')
    outfile = open(output_filename, 'w')

    try:
        # Setup stream parameters
        acquisition_frequency = stream_rate
        stream_frequency = 10   #Hz
        vectors_per_sample = len(parameter_list)
        floats_per_vector = 3
        registers_per_float = 2
        bytes_per_register = int(calcsize('H'))
        bytes_per_sample = vectors_per_sample * floats_per_vector * registers_per_float * bytes_per_register
        samples_per_box = acquisition_frequency / stream_frequency #int(800 / 10 / (1 << stream_rate_config)) #800Hz, target 10Hz
        content_bytes = samples_per_box * bytes_per_sample
        box_bytes = 4 + content_bytes + 2   # 2 start bytes, 2 count bytes, content bytes, 2 crc bytes
        previous_packet_count = -1

        # Process input stream
        state = 0
        rxbytes = bytearray()
        # Print data header
        header = 'Packet Count, Delta Time,'
        stream_param_headers = []
        for param in parameter_list:
            stream_param_headers.append(param + ' X')
            stream_param_headers.append(param + ' Y')
            stream_param_headers.append(param + ' Z')
        for elem in stream_param_headers:
            header += str(elem) + ','
        header += 'CRC'
        print('{}'.format(header))
        outfile.write(header + '\n')
        # Go through file and parse each byte
        byte = infile.read(1)
        # If byte is not null, process through state machine
        while byte != b'':
            b = int.from_bytes(byte, byteorder='big')
            # State 0: waiting for first start byte
            if (state == 0):
                # if (b == b'\xfe'):
                if (b == 0xFE):
                    state += 1
                    rxbytes = bytearray()
                    rxbytes.append(b)
            # State 1: waiting for second start byte
            elif (state == 1):
                # if (b == b'\xed'):
                if (b == 0xED):
                    state += 1
                    rxbytes.append(b)
                # elif (byte == b'\xfe'):
                elif (b == 0xFE):
                    state = 1
                else:
                    state = 0
            # State 2: waiting for remainder of box
            elif (state == 2):
                rxbytes.append(b)
                if (len(rxbytes) >= box_bytes):
                    # Check CRC for data integrity
                    crc = 0xFFFF
                    for elem in rxbytes[0:int(box_bytes)]:
                        crc = update_crc(crc, elem)
                    # Extract packet count
                    packet_count = rxbytes[2] << 8 | rxbytes[3]
                    # Begin decoding packet contents
                    # Decode contents to float values
                    content_buffer = rxbytes[4:-2]
                    value_buffer = []
                    i = 0
                    while (i < len(content_buffer)/4):
                        value = unpack('<f', content_buffer[4*i : 4*i+4])[0]
                        value_buffer.append(value)
                        i += 1
                    # Format values into string
                    debug_output = ''
                    line_count_max = (vectors_per_sample * floats_per_vector) # floats per line
                    delta_time = 0
                    if (previous_packet_count == -1):
                        previous_packet_count = packet_count - 1
                    delta_time_offset = (packet_count - (previous_packet_count + 1))*0.10
                    previous_packet_count = packet_count
                    vectors = []
                    for i in range(vectors_per_sample):
                        vectors.append([0.0, 0.0, 0.0])
                    for i in range(len(value_buffer)):
                        # sample_count = index of sample in packet
                        sample_count = i / (vectors_per_sample * floats_per_vector)
                        float_count = i % (vectors_per_sample * floats_per_vector)

                        if (i % line_count_max == 0):
                            # Calculate the delta time:
                            #   - Each packet comes every 0.100s (10Hz)
                            #   - Each sample comes in at rate determined by stream_rate_config
                            delta_time = delta_time_offset + 1/float(acquisition_frequency)
                            # Reset delta time offset
                            delta_time_offset = 0
                        
                        vectors[int(float_count / floats_per_vector)][int(float_count % floats_per_vector)] = value_buffer[i]
                        if (i % line_count_max == (line_count_max - 1)):
                            debug_output += '{:d}, {:.3f}'.format(packet_count, delta_time)
                            for i in range(vectors_per_sample):
                                for j in range(3):
                                    debug_output += ', {:+2.4f}'.format(vectors[i][j])
                            debug_output += ', {}\n'.format(crc)
                            print(debug_output)
                    # Reset state to 0
                    state = 0
                    # Write and flush output string to file
                    outfile.write(debug_output)
                    outfile.flush()

            # Read next byte
            byte = infile.read(1)
        
        outfile.close()
        infile.close()
    except KeyboardInterrupt:
        outfile.close()
        infile.close()
        return
    
crc_table = None
def __crc_table_init():
    global crc_table
    # Initialize crc_table
    crc_table = list(range(256))
#	print('crc table before: {}'.format(crc_table))
    for i in range(0,256):
        crc = 0
        c = i
        for j in range(0, 8):
            if ((crc ^ c) & 0x0001):
                crc = (crc >> 1) ^ 0xA001
            else:
                crc = crc >> 1
            c = c >> 1
        crc_table[i] = crc
#	print('crc table after: {}'.format(crc_table))

def update_crc(crc, c):
    global crc_table
    int_c = 0x00ff & c
    if (crc_table is None):
        # Initialize table
        __crc_table_init()
    tmp = crc ^ int_c
    crc = (crc >> 8) ^ crc_table[tmp & 0xff]
    return crc



def yaw(R):
    return np.arctan2(-R[0,1],R[1,1])*57.3 

def pitch(R):
    return np.arctan2(R[2,1],np.sqrt(R[1,0]*R[1,0]+R[1,1]*R[1,1]))*57.3 

def roll(R):
    return np.arctan2(-R[2,0],R[2,2])*57.3 

    

class IMOS():
    """
    Transmitter class for talking to IMOS sensors

    Args:
        * param1: 
        * param2:

    """
    
    #set up sensor object
    def __init__(self, port, baudrate=115200, timeout=1):
        self.modbus = Instrument(port, SLAVEADDRESS)
        self.modbus.serial.parity = PARITY
        self.modbus.serial.baudrate = baudrate
        self.modbus.serial.timeout = timeout
        self.dictionary()
        self.R_ref = np.matrix([[1,0,0],[0,1,0],[0,0,1]])
    
    #change the baudrate once you have connected at the current baudrate 
    def set_baudrate(self, baudrate):
        rate = self.baudrate_check(baudrate)
        print(rate)
        self.modbus_write(self.main_dictionary['baudrate']['address'],rate)
        self.modbus_write_flash()
        self.modbus.serial.baudrate = baudrate
    
    #making baudrate values conform to what the register values should be
    def baudrate_check(self, baudrate):
        if baudrate == 1200:
            rate = 0x0001
        elif baudrate == 2400:
            rate = 0x0101
        elif baudrate == 4800:
            rate = 0x0201
        elif baudrate == 9600:
            rate = 0x0301
        elif baudrate == 19200:
            rate = 0x0401
        elif baudrate == 38400:
            rate = 0x0501
        elif baudrate == 57600:
            rate = 0x0601
        elif baudrate == 115200:
            rate = 0x0701
        elif baudrate == 230400:
            rate = 0x0801
        elif baudrate == 460800:
            rate = 0x0901
        elif baudrate == 921600:
            rate = 0x0A01
        else:
            rate = 0x0701
        return rate 

    #Print the firmware version 
    def get_version(self):
        try:
            fw_arr = self.read('version')
            print('Device firmware: v{:d}.{:02d}'.format(fw_arr[1], fw_arr[0]))
        except KeyError:
            # Initial firmware release does not have version in it's device dictionary
            print('Device firmware: v0.01')
    
    #disconnect from the IMOS sensor
    def disconnect(self):
        self.modbus.serial.close()
    
    #read any value by naming it, can read calibrated and uncalibrated values
    def read(self, key, calibrated=True, JSON=False):
        serialization = self.main_dictionary[key]['serialization']
        if calibrated:
            address = self.main_dictionary[key]['address']
        else:
            key = "$" + key
            address = self.main_dictionary[key]['address']
        try:
            self.modbus.serial.reset_input_buffer()
            self.modbus.serial.reset_output_buffer()
            return unpack(serialization, self.modbus_read(address, calcsize(serialization)))
        except IOError as e:
            print(e)
            return None

    # write any value by naming it
    def write(self, key, value):
        # lookup the serialization for the value to be written
        serialization = self.main_dictionary[key]['serialization']
        # pack the value into a binary string
        try:
            bytes = pack(serialization, value)
        except:
            try:
                bytes = pack(serialization, *value)
            except:
                print ('error writing value')
                return
        # lookup the address for where to write the data
        address = self.main_dictionary[key]['address']
        # this is modbus, so we write in 16-bit registers
        n_registers = int(calcsize(serialization)/2)
        registers = list(unpack(str(n_registers)+'H', bytes))
        # actually write the data
        try:
            self.modbus.serial.reset_input_buffer()
            self.modbus.serial.reset_output_buffer()
            self.modbus.write_registers(address,registers)
        except IOError as e:
            print(e)
            return None

    
    #this checks for timeouts
    def __timeout_checker(self, startTime, currTime, timeout=5):
        if (currTime - startTime) >= timeout:
            raise TimeoutError
        
    #set up the dictionary before trying to use it in later functions
    def dictionary(self, printStream=False):
        self.modbus.custom_command(0x01, 0x00)
        rxbytes = bytearray()
        try:
            lastReadTime = time.time()
            while True:
                bytes_to_read = self.modbus.serial.inWaiting() #shows number of bytes to receive
                if (bytes_to_read == 0):
                    # Check if timeout exceeded
                    self.__timeout_checker(lastReadTime, time.time())
                if (bytes_to_read > 0):
                    # Update read time to current time
                    lastReadTime = time.time()
                    # Read response in serial port
                    response = self.modbus.serial.read(bytes_to_read) #reads the bytes
                    if (0 in response):
                        # Remove null character from string
                        temp = list(response)
                        temp.remove(0)
                        response = bytes(temp)
                        # Append response to string and exit loop
                        rxbytes.extend(response)
                        break
                    else:
                        rxbytes.extend(response)
        except KeyboardInterrupt:
            return 0
        # Remove extraneous elements that are non-ascii and not part of the JSON string
        text = ''
        braceCounter = 0
        for elem in rxbytes:
            if elem < 128:
                # If string is currently empty
                if (not text.strip()):
                    # If next element is not a starting brace, ignore
                    if (chr(elem) != '{'):
                        pass
                    # Otherwise, add to text and increment brace counter
                    else:
                        braceCounter += 1
                        text += chr(elem)
                # If string is not currently empty
                else:
                    # If next element is an opening curly brace, increment brace counter
                    if (chr(elem) == '{'):
                        braceCounter += 1
                    # Else if next element is a closing curly brace, decrement brace counter
                    elif (chr(elem) == '}'):
                        braceCounter -= 1
                    # Add element to string
                    text += chr(elem)
                    # If brace counter is zero, we have finished our json string and can exit
                    if (braceCounter == 0):
                        break
        if (printStream):
            print(text)
        self.main_dictionary = json.loads(text)
        return self.main_dictionary

    #gives the list of possible measurements
    def measurements(self):
        # Update internal dictionary
        self.dictionary()
        # Create subset with just measurement type keys
        subdict = dict()
        for key in self.main_dictionary.keys():
            datatype = self.main_dictionary[key]['type']
            if (datatype == 'measurement'):
                subdict[key] = self.main_dictionary[key]
        # Return sub dictionary
        return subdict       

    #gives the list of possible calibration coefficients for each sensor
    def coefficients(self):
        # Update internal dictionary
        self.dictionary()
        # Create subset with just measurement type keys
        subdict = dict()
        for key in self.main_dictionary.keys():
            datatype = self.main_dictionary[key]['type']
            if (datatype == 'calibration_coefficient'):
                subdict[key] = self.main_dictionary[key]
        # Return sub dictionary
        return subdict   
    
    #sets up streaming rate and which measurements to stream. Can take multiple measurement args.
    def setup_stream(self, measurements, streamRate=100, saveToFlash=True):
        # print("number of args",len(arg))
        rate = self.__stream_rate_check(streamRate)
        # print("stream rate is", rate)
        address = self.main_dictionary['stream_data']['address']
        for a in measurements:
            # print(a)
            targetAddress = self.main_dictionary[a]['address']
            for i in range(0,6):
                self.modbus_write_val(address, targetAddress, 'H') #write target register address to streaming register
                address += 1
                targetAddress += 1            
        self.modbus_write(self.main_dictionary['stream_rate']['address'], rate) #set the streaming rate based on config table
        n_registers = len(measurements) * 6
        self.modbus_write_val(self.main_dictionary['num_to_stream']['address'], n_registers, 'H') #set how many registers to stream
        if (saveToFlash):
            self.modbus_write_flash()
        
        
    #converting streaming rate in Hz to the right code 
    def __stream_rate_check(self, streamRate):
        if (streamRate == 800):
            streamRate = 0x0000
        elif streamRate == 400:
            streamRate = 0x0001
        elif streamRate == 200:
            streamRate = 0x0002
        elif streamRate == 100:
            streamRate = 0x0003
        else:
            streamRate = 0x0003 #default is 100Hz
        return streamRate
    
    
    #starts streaming, pass the desired function to perform for every data sample
    def start_stream(self, param1, param2, param3, stream_rate, update_function=None, saveToFlash=False):
        """Start and parse the data from stream mode into readable floats. Assumes that the device has been set to stream 3 vectors

        Args:
            * param1 (string): Name of first parameter to stream
            * param2 (string): Name of second parameter to stream
            * param3 (string): Name of third parameter to stream
            * stream_rate (integer): Frequency at which to stream data at (100Hz, 200Hz, 400Hz, 800Hz)
            * update_function (function): Function to call when a set of data is retrieved
            * saveToFlash (boolean): Boolean to indicate whether or not to save stream settings to flash

        """
        if param1 is None or param2 is None or param3 is None:
            raise ValueError('Parameter names cannot be "None"')
        if stream_rate != 100 and stream_rate != 200 and stream_rate != 400 and stream_rate != 800:
            raise ValueError('{} is not a supported stream rate'.format(stream_rate))
        try:
            # Setup device stream
            print('Setting up device stream...')
            self.setup_stream([param1, param2, param3],stream_rate, saveToFlash=False) 

            # Setup stream parameters
            acquisition_frequency = 800 / (1 << self.read('stream_rate')[0])
            stream_frequency = 10   #Hz
            vectors_per_sample = 3
            floats_per_vector = 3
            registers_per_float = 2
            bytes_per_register = int(calcsize('H'))
            bytes_per_sample = vectors_per_sample * floats_per_vector * registers_per_float * bytes_per_register
            samples_per_box = acquisition_frequency / stream_frequency #int(800 / 10 / (1 << stream_rate_config)) #800Hz, target 10Hz
            content_bytes = samples_per_box * bytes_per_sample
            box_bytes = 4 + content_bytes + 2   # 2 start bytes, 2 count bytes, content bytes, 2 crc bytes
            previous_packet_count = -1

            # Send custom command to start stream
            self.modbus.custom_command(0x00, 0x01)
            self.modbus_start_stream(saveToFlash=saveToFlash)

            # Process input stream
            state = 0
            rxbytes = bytearray()
            # Print data header
            header = 'Delta Time,'
            stream_param_headers = (
                param1 + ' X', param1 + ' Y', param1 + ' Z',
                param2 + ' X', param2 + ' Y', param2 + ' Z',
                param2 + ' X', param2 + ' Y', param2 + ' Z',             
            )
            for elem in stream_param_headers:
                header += str(elem) + ','
            header += 'CRC'
            print('{}'.format(header))
            # Loop to wait for and parse incoming serial data 
            while True:
                bytes_to_read = self.modbus.serial.inWaiting()
                if (bytes_to_read > 0):
                    response = self.modbus.serial.read(bytes_to_read)
                    # print(response)
                    # Go throught byte by byte
                    for b in response:
                        # State 0: waiting for first start byte
                        if (state == 0):
                            if (b == 0xFE):
                            # if (b == b'\xfe'):
                                state += 1
                                rxbytes = bytearray()
                                rxbytes.append(b)
                        # State 1: waiting for second start byte
                        elif (state == 1):
                            if (b == 0xED):
                            # if (b == b'\xed'):
                                state += 1
                                rxbytes.append(b)
                            elif (b == 0xFE):
                            # elif (b == b'\xfe'):
                                state = 1
                            else:
                                state = 0
                        # State 2: waiting for remainder of box
                        elif (state == 2):
                            rxbytes.append(b)
                            if (len(rxbytes) >= box_bytes):
                                # Check CRC for data integrity
                                crc = 0xFFFF
                                for elem in rxbytes[0:int(box_bytes)]:
                                    crc = update_crc(crc, elem)
                                # Extract packet count
                                packet_count = rxbytes[2] << 8 | rxbytes[3]
                                # Begin decoding packet contents
                                # Decode contents to float values
                                content_buffer = rxbytes[4:-2]
                                value_buffer = []
                                i = 0
                                while (i < len(content_buffer)/4):
                                    value = unpack('<f', content_buffer[4*i : 4*i+4])[0]
                                    value_buffer.append(value)
                                    i += 1
                                # Format values into string
                                line_count_max = (vectors_per_sample * floats_per_vector) # floats per line
                                delta_time = 0
                                delta_time_offset = (packet_count - (previous_packet_count + 1))*0.10
                                previous_packet_count = packet_count
                                vectors = [
                                    [0.0, 0.0, 0.0],
                                    [0.0, 0.0, 0.0],
                                    [0.0, 0.0, 0.0],
                                ]
                                for i in range(len(value_buffer)):
                                    # sample_count = index of sample in packet
                                    sample_count = i / (vectors_per_sample * floats_per_vector)
                                    float_count = i % (vectors_per_sample * floats_per_vector)

                                    if (i % line_count_max == 0):
                                        # Calculate the delta time:
                                        #   - Each packet comes every 0.100s (10Hz)
                                        #   - Each sample comes in at rate determined by stream_rate_config
                                        delta_time = delta_time_offset + 1/float(acquisition_frequency)
                                        # Reset delta time offset
                                        delta_time_offset = 0
                                    
                                    vectors[int(float_count / floats_per_vector)][int(float_count % floats_per_vector)] = value_buffer[i]
                                    if (i % line_count_max == (line_count_max - 1)):
                                        debug_output = '{:.3f}'.format(delta_time)
                                        for i in range(3):
                                            for j in range(3):
                                                debug_output += ', {:+2.4f}'.format(vectors[i][j])
                                        # print(debug_output)
                                        if update_function is not None:
                                            update_function(delta_time, vectors[0], vectors[1], vectors[2])
                                # Reset state to 0
                                state = 0
        except KeyboardInterrupt:
            self.stop_stream()
            return
    
    #sets the device to streaming mode
    def modbus_start_stream(self, saveToFlash=False):
        # Send custom command to start streaming
        self.modbus.custom_command(0x00, 0x01)
        # Save to flash if desired
        if (saveToFlash):
            self.modbus_write_flash()
        print("Starting streaming")
    
    #stop streaming
    def stop_stream(self, saveToFlash=False):
        # Send custom command to stop streaming
        self.modbus.custom_command(0x00, 0x00)
        rxbytes = bytearray()
        try:
            while True:
                startTime = time.time()
                bytes_to_read = self.modbus.serial.inWaiting()
                if (bytes_to_read > 0):
                    response = self.modbus.serial.read(bytes_to_read)
                    if (bytes_to_read == 0):
                        self.__timeout_checker(startTime, time.time())
                    if (0 in response):
                        # Remove null character from string
                        temp = list(response)
                        temp.remove(0)
                        response = bytes(temp)
                        # Append response to string and exit loop
                        rxbytes.extend(response)                        
                        text = ''
                        for elem in rxbytes:
                            if elem < 128:
                                text += chr(elem)
                        # for elem in rxbytes.decode('utf-8').strip():
                        #     text += elem
                        print(text)
                        break
                    else:
                        rxbytes.extend(response)
        except KeyboardInterrupt:
            pass
        # Save to flash if desired
        if (saveToFlash):
            self.modbus_write_flash()
    
    #modbus command to stop streaming 
    def modbus_stop_stream(self):
        self.modbus.custom_command(0x00, 0x00)
        print("Stopping streaming")

    #modbus command to restart the device
    def modbus_restart_device(self):
        self.modbus.custom_command(0x02, 0x00)
        print('Restarting device...')
        time.sleep(10)
        print('Complete!')

    #modbus command to save settings to flash
    def modbus_write_flash(self):
        self.modbus.custom_command(0x02, 0x01)
        print('Writing settings to flash...')
        time.sleep(10)
        print('Complete!')

    #modbus command to factory reset device to restore default settings
    def modbus_factory_reset(self):
        self.modbus.custom_command(0x02, 0x7F)
        print('Resetting device to factory defaults...')
        time.sleep(10)
        print('Complete!')
    
    #modbus for reading the number of bytes you want
    def modbus_read(self, address, n_bytes): #2 addresses are 4 bytes which is 2 registers
        # Get # of registers (each register is 16-bits which is 2-bytes)
        n_registers = n_bytes/2
        bytearr = bytearray()
        # Read register values
        values = self.modbus.read_registers(address, int(n_registers))
        # Reconstruct byte array
        for elem in values: 
            bytearr.append(0x00FF & elem)
            bytearr.append((0xFF00 & elem) >> 8)
        # Return read bytes
        return bytearr
    
    #writes a value (proper number) to the given address based on serialization format
    def modbus_write_val(self, address, value, serialization): #takes a value to write
        n_registers = int(calcsize(serialization)/2) #number of registers to writee to
        compartments = [None]*n_registers #a containter for the value
        modValue = pack(serialization,value) #convert the value to the correct serialization in bytes
        #now modify the bytes so the input format is right 
        i = 0
        j = 0
        #this feels like it shouldn't work but it does.
        while i <= n_registers:
            (compartments[j],) = unpack('H',modValue[i:i+2]) #separate the bytes into registers and put them into the 0-65536 range
            i += 2
            j += 1
        try:
            self.modbus.write_registers(address,compartments)
        except IOError:
            print('IOError occurred while writing...')
        except ValueError:
            print('ValueError occurred while writing...')
 
           
     #modbus command to write a byte to a given address       
    def modbus_write(self, address, byteToWrite):
        try:
            self.modbus.write_register(address, byteToWrite)
        except IOError:
            print('IOError occurred while writing...')
        except ValueError:
            print('ValueError occurred while writing...')
 
    
    #load calibration coefficients, calTable is a dictionary        
    def load_calibration(self, calTable, saveToFlash=True):
        print(calTable.keys())
        #print(calTable.values())
        c = self.coefficients()
        for key in calTable.keys():
            #get the address for gamma and beta values of that sensor, then write the coefficient values to memory
            gammaKey = key + "_gamma"
            gammaAddress = c[gammaKey]['address']
            betaKey = key + "_beta"
            betaAddress = c[betaKey]['address']
            for i in range(0,9):
                gammaToWrite = calTable[key]['gamma'][i]
                gammaSerialization = self.main_dictionary[gammaKey]['serialization'][i]
                self.modbus_write_val(gammaAddress,gammaToWrite,gammaSerialization)
                gammaAddress += 2
                if (i < 3): #there are only 3 beta values
                    betaToWrite = calTable[key]['beta'][i]
                    betaSerialization = self.main_dictionary[betaKey]['serialization'][i]
                    self.modbus_write_val(betaAddress,betaToWrite,betaSerialization)
                    betaAddress += 2
        if (saveToFlash):
            self.modbus_write_flash()

    
    #read the calibration coefficient values
    def dump_calibration(self):
        c = self.coefficients()
        data = collections.defaultdict(dict) #setting up the dictionary
        for key in c.keys():
            address = c[key]['address']
            serialization = self.main_dictionary[key]['serialization']
            value = unpack(serialization, self.modbus_read(address,calcsize(serialization)))
            if key.endswith("_gamma"):
                outerKey = key[:-6]
                innerKey = "gamma"
            elif key.endswith("_beta"):
                outerKey = key[:-5]
                innerKey = "beta"
            data[outerKey][innerKey] = value
        return dict(data) #data is a dictionary with key-value pairs where you can access elements by name
   

    #save calibration coefficient values to output JSON file
    def save_calibration_to_file(self, filename):
        if (not filename.endswith('.json')):
            filename += '.json'
        print('Writing calibration data to: {}'.format(filename))
        file = open(filename, 'w')
        cal = json.dumps(self.dump_calibration())
        file.write('{}'.format(cal))
        file.flush()
        file.close()
        print('Save complete!')


    #load calibration coefficients values from JSON file to device
    def load_calibration_from_file(self, filename, saveToFlash=False):
        print('Parsing file to form calibration table...')
        if (not filename.endswith('.json')):
            raise TypeError('Calibration file must be a .json file')
        file = open(filename, 'r')
        jsonconfig = file.read()
        dictionary = json.loads(jsonconfig)
        print('Loading calibration data to IMOS...')
        self.load_calibration(dictionary, saveToFlash=saveToFlash)
        print('Load complete!')


    # print the specified vector nicely to the stream
    def poll(self, vector, smoothing=1):
        y_avg = [0,0,0]
        try:
            n=0
            while True:
                if (n < smoothing):
                    n += 1
                y = self.read(vector)
                for i in (0,1,2):
                    y_avg[i] += (y[i] - y_avg[i]) / n
                print('\r[ x = %7.3f, y = %7.3f, z = %7.3f ]' % tuple(y_avg) , end='', flush=True)
        except:
            print('')
            return


    def stdev(self, vector, smoothing=100):
        y_avg = [0,0,0]
        y_variance = [0,0,0]
        y_stdev = [0,0,0]
        try:
            n=0
            while True:
                if (n < smoothing):
                    n += 1
                y = self.read(vector)
                for i in (0,1,2):
                    f = y[i] - y_avg[i]
                    y_avg[i] += f / n
                    y_variance[i] += (f**2 - y_variance[i]) / smoothing
                    y_stdev[i] = sqrt(y_variance[i])
                print('\r[ x = %7.3f, y = %7.3f, z = %7.3f ]' % tuple(y_stdev) , end='', flush=True)
        except:
            print('')
            return

    def angles(self):
        try:
            while True:
                Rl = self.read('R')
                R = np.matrix([Rl[0:3], Rl[3:6], Rl[6:9]])
                R_rel = self.R_ref*R
                print('\r[ x = %7.3f, y = %7.3f, z = %7.3f ]' % (yaw(R_rel), pitch(R_rel), roll(R_rel)) , end='', flush=True)
        except:
            print('')
            return

    def zeroAngles(self):
        Rl = self.read('R')
        R = np.matrix([Rl[0:3], Rl[3:6], Rl[6:9]])
        self.R_ref = R**-1

    def zero_gyroscope_2000(self, samples=100):
        offset = np.matrix(self.read('gyroscope_2000_beta'))
        error = np.matrix((0.,0.,0.))
        for i in range(samples):
            error += np.matrix(self.read('gyroscope_2000'))
        null = error / samples
        self.write('gyroscope_2000_beta', (offset + null).tolist()[0])

    def zero_gyroscope_600(self, samples=100):
        offset = np.matrix(self.read('gyroscope_600_beta'))
        error = np.matrix((0.,0.,0.))
        for i in range(samples):
            error += np.matrix(self.read('gyroscope_600'))
        null = error / samples
        self.write('gyroscope_600_beta', (offset + null).tolist()[0])