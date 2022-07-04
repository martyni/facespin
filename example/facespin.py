#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
from random import randint, choice
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.CRITICAL)
Picture = '../../Pictures/alexanderjnewall.png'

def average(lst):
   return sum(lst) / len(lst)

def transform(image, amount, flag='rotate'):
    if flag=='rotate':
        logging.info("Rotating {}".format(amount))
        return image.rotate(amount)
    elif flag=='spread':
        logging.info("spread {}".format(amount))
        return image.effect_spread(amount)
    elif flag=='mandelbrot':
        if amount < 0:
            amount -= amount
        logging.info("mandelbrot {}".format(amount))
        paste = Image.effect_mandelbrot( 
                (amount, amount), 
                (amount, amount, amount, amount),
                quality=100
                )
        image.paste(paste )
        return image
    elif flag=='noise':
        if amount < 0:
            amount -= amount
        logging.info("noise {}".format(amount))
        paste = Image.effect_noise((240,amount ), amount)
        image.paste(paste, ( 0 , 240 - amount))
        return image
    elif flag=='resize':
        logging.info("resize {}".format(amount))
        if amount < 0:
            amount -= amount
        if amount < 1:
            amount = 1
        paste = image.resize((amount,amount))
        image.paste(paste, ( int(120 - amount /2) , 240 - amount))
        return image

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch28.LCD_1inch28()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    logging.info("show image")
    image = Image.open(Picture)
    amount = 90
    spun = 0
    speed = 1
    previous_speeds = [1]
    flag = 'noise'
    while True:
       im_r=transform(image, amount, flag=flag)
       disp.ShowImage(im_r)
       amount += speed
       if  amount >= 360 or amount <= -360:
          amount = 0
          spun += 1
          avg = average(previous_speeds)
          logging.info("Spun {} times \nSpeed was {}\navg speed is {}".format(spun, speed, avg))
          speed = randint(-10, 10)
          previous_speeds.append(int(speed))
          if len(previous_speeds) > 1000:
              previous_speeds.pop(0)
          speed = 1 if not speed else speed
          flag = choice(['spread', 'rotate', 'noise', 'resize'])
          image = Image.open(Picture)	
    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.critical(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
