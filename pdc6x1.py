# Sevensegment LCD display with 6 digits/characters with 3 precision decimal
# points and 3 level battery indicator. The LCD display is mostly tagged as
# PDC6x1, driven by the HT1621 chip.
#
# This class is developed for raspberry pi and uses the SPI driver.
# Make sure SPI is enabled in raspi-config.
#
# To understand the inner workings of this class study the HT1621 datasheet.
#
# Tested on: PI 3B+ Rev 1.3, Raspian Buster.
# last change: 8 dec 2019
#
#
# Reused the segment_mapper from the luma.lcd project from
# Richard Hull and contributors. no changes made. 
#
#
#
# Copyright (c) 2019 Erik Gordebeke, Jules Leijnen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# Basically, we got the class working by studying the HT1621 datasheet and
# by researching information on the internet. So, ...
#
# You are free to reproduce, distribute, interpret, misinterpret, distort, garble,
# do what you like, even claim authorship, without our consent or the permission of
# anybody. We really do not care :)
#
#
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import spidev
import segment_mapper

DEBUG = 1


class PDC6x1:

    def __init__(self):

        self._spi = spidev.SpiDev()
        self._spi.open(bus=0, device=0)
        self._spi.cshigh = False
        self._spi.max_speed_hz = 1000000
        self._spi.mode = 0

        # reset display by sending disable command
        self._spi.writebytes([0x80, 0x00])

        # initialise display with config:
        # read bytes in list as continuous bits
        # 3bits cmd (100) with 8 bits per config
        # split over bytes resuls in numbers in list
        # cmd, rc256, enable, bias1/3-4commons, lcd on
        self._spi.writebytes([0x80, 0x22, 0x90, 0x18, 0x30])



    def _convert_digits(self, digits):

        # create empty data buffer for the 6 digits
        data_buffer = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        # data buffer index, digits are loaded from right to left
        i = 5

        for digit in segment_mapper.dot_muncher(digits):

            data_buffer[i] = digit
            i -= 1

        return data_buffer



    def _prep_data(self, data_bits, value, num_bits):

        # collect all bits in  data_bits and return

        for _ in range(num_bits):

            data_bits <<= 1

            if (value & 0x80): data_bits += 1

            value <<= 1

        return data_bits



    def _data(self, data_buffer):

        # bits are collected in data_bits (integer) through prep_data()
        # 8 bytes in total

        data_bits = 0   # init as int

        data_bits = self._prep_data(data_bits, 0xA0, 3)   # collect 3 bits ('101...')
        data_bits = self._prep_data(data_bits, 0x00, 6)   # pad address with 6 bits


        # process data buffer
        for digit in data_buffer:
           data_bits = self._prep_data(data_bits, digit, 8)


        data_bits = self._prep_data(data_bits, 0x00, 7)   # pad to complete byte with 7 bits

        return data_bits



    def _send_data(self, data_bits):
          # todo:  check writebytes instead of xfer2
          self._spi.xfer2( data_bits.to_bytes(8,byteorder='big') )



    # decimal_point 0 is the point closes to the battery level indicator
    # battery_level: 0 means first indication, 2 is fully lit
    #
    def show(self, digits, decimal_point = -1, battery_level = -1):

        # check inputs
        if decimal_point not in range(-1, 2): raise ValueError("decimal_point must be 0, 1 or 2")
        if battery_level not in range(-1, 2): raise ValueError("battery_level must be 0, 1 or 2")

        # text bigger than 6 digits/ chars is not considered an error
        # just not usefull for this display.
        # take first 6 digits/ chars of text, ignore the rest.
        # convert text to sevendigit bytes and fill data_buffer
        if len( digits ) > 6 :
                digits = digits[:6]


        # convert text to lcd digits
        data_buffer = self._convert_digits( digits )


        # decimal point is first bit of first three bytes in data_buffer
        # 'OR' the bit onto the byte with bitmask. idem for battery_level
        #
        # value decimalpoint is same als data_buffer index

        if decimal_point != -1 :
            data_buffer[decimal_point] |= 0x80


        # set battery_level

        if battery_level != -1 :

            data_buffer[3] |= 0x80

            if battery_level > 0:
                data_buffer[4] |= 0x80

                if battery_level == 2:
                   data_buffer[5] |= 0x80


        #unittest: print content of data_buffer
        if DEBUG:
            print("----------------------")
            print("---- {} ----------".format(digits))

            for d in data_buffer:
                print("-->   0x{:02x}".format(d))


        # collect the data bits to send to display
        data_bits = self._data(data_buffer)


        #unittest: print content of data_bits
        if DEBUG:
            print("----------------------")
            print("-->   0x{:02x}".format(data_bits))



        # send_data
        self._send_data(data_bits)








