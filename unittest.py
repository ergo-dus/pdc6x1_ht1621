#!/usr/bin/python3


# UNIT_TEST file for: 
#
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
#
#
#
# Copyright (c) 2019 Erik Gordebeke
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


#unit tests

import sys
import getopt
import pdc6x1


def show_error():
      print ('usage: unittest.py -d <digits> -p <decimal_point (0,1,2) > -b <battery_level (0,1,2)')
      sys.exit(2)


def main(argv):

    #default values
    digits = ""
    decimal_point = -1
    battery_level = -1


    try:
        opts, args = getopt.getopt(argv,"hd:p:b:")

        if len(argv) < 2: show_error()

    except getopt.GetoptError:
        show_error()

    for opt, arg in opts:
        if opt == '-h':
            show_error()
        elif opt == '-d':
            digits = arg
        elif opt == '-p':
            decimal_point = int(arg)
        elif opt == '-b':
            battery_level = int(arg)


    print(digits, decimal_point, battery_level)

    display = pdc6x1.PDC6x1()
    display.show(digits, decimal_point, battery_level)




if __name__ == '__main__':
        main(sys.argv[1:])

