# pdc6x1_ht1621
python 'driver' for the 6digit 7segment lcd display known as pdc6x1 driven by the ht1621 chip for raspberry pi. Python class uses the SPI interface.


connect to raspberry pi 3+ with pins

GND   Ground                P01-06 GND
VCC   +3.3V Power           P01-01 3V3
DAT   SPI data              P01-19 GPIO 10 (MOSI)
WR    SPI clock             P01-23 GPIO 11 (SCLK)
CS    SPI chip select       P01-24 GPIO 8 (CE0)
LED   Backlight control     P01-12 GPIO 18 (PCM_CLK)
