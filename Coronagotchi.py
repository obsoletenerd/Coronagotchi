#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

# This assumes you already have the Waveshare EPD running and the libraries installed
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13bc
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG)

# Source:       https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data

# Grab the latest CSV files
os.system("wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv -O confirmed.csv")
os.system("wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv -O deaths.csv")
os.system("wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv -O recovered.csv")
file_confirmed = r'confirmed.csv'
file_deaths = r'deaths.csv'
file_recovered = r'recovered.csv'
# TODO: Do this better, with error handling and naming them based on time/date download


##
# INFECTED
##

# Load the CSV
cvc_df = pd.read_csv(file_confirmed)

# Find the last columns (stats from last few days)
cv_today_col = len(cvc_df.columns) - 1
cv_1ago_col = len(cvc_df.columns) - 2
cv_2ago_col = len(cvc_df.columns) - 3
cv_3ago_col = len(cvc_df.columns) - 4
cv_4ago_col = len(cvc_df.columns) - 5
cv_5ago_col = len(cvc_df.columns) - 6
cv_6ago_col = len(cvc_df.columns) - 7

# Load the CSV filtering it to just show the columns/rows we want
cvc_df = pd.read_csv(file_confirmed, usecols=[0, 1, cv_today_col, cv_1ago_col, cv_2ago_col, cv_3ago_col, cv_4ago_col, cv_5ago_col, cv_6ago_col])
cvc_df_au = cvc_df[cvc_df["Country/Region"].str.contains("Australia")]

# Add up the numerical columns
cv_sums = cvc_df_au.sum(axis=0, numeric_only=True)

# Load up the last week of totals
cv_today = int(round(cv_sums.iloc[6]))
cv_1ago = int(round(cv_sums.iloc[5]))
cv_2ago = int(round(cv_sums.iloc[4]))
cv_3ago = int(round(cv_sums.iloc[3]))
cv_4ago = int(round(cv_sums.iloc[2]))
cv_5ago = int(round(cv_sums.iloc[1]))
cv_6ago = int(round(cv_sums.iloc[0]))


##
# RECOVERED
##

# Load the CSV
cvr_df = pd.read_csv(file_recovered)

# Find the last columns (stats from last few days)
cvr_today_col = len(cvr_df.columns) - 1
cvr_1ago_col = len(cvr_df.columns) - 2
cvr_2ago_col = len(cvr_df.columns) - 3
cvr_3ago_col = len(cvr_df.columns) - 4
cvr_4ago_col = len(cvr_df.columns) - 5
cvr_5ago_col = len(cvr_df.columns) - 6
cvr_6ago_col = len(cvr_df.columns) - 7

# Load the CSV filtering it to just show the columns/rows we want
cvr_df = pd.read_csv(file_recovered, usecols=[0, 1, cvr_today_col, cvr_1ago_col, cvr_2ago_col, cvr_3ago_col, cvr_4ago_col, cvr_5ago_col, cvr_6ago_col])
cvr_df_au = cvr_df[cvc_df["Country/Region"].str.contains("Australia")]

# Add up the numerical columns
cvr_sums = cvr_df_au.sum(axis=0, numeric_only=True)

# Load up the last week of totals
cvr_today = int(round(cvr_sums.iloc[6]))
cvr_1ago = int(round(cvr_sums.iloc[5]))
cvr_2ago = int(round(cvr_sums.iloc[4]))
cvr_3ago = int(round(cvr_sums.iloc[3]))
cvr_4ago = int(round(cvr_sums.iloc[2]))
cvr_5ago = int(round(cvr_sums.iloc[1]))
cvr_6ago = int(round(cvr_sums.iloc[0]))


##
# DEATHS
##

# Load the CSV
cvd_df = pd.read_csv(file_deaths)

# Grab just the last column for latest death total
cvd_today_col = len(cvd_df.columns) - 1
cvd_1ago_col = len(cvd_df.columns) - 2
cvd_2ago_col = len(cvd_df.columns) - 3
cvd_3ago_col = len(cvd_df.columns) - 4
cvd_4ago_col = len(cvd_df.columns) - 5
cvd_5ago_col = len(cvd_df.columns) - 6
cvd_6ago_col = len(cvd_df.columns) - 7

# Load the deaths CSV and filter it to Australia
cvd_df = pd.read_csv(file_deaths, usecols=[0, 1, cvd_today_col, cvd_1ago_col, cvd_2ago_col, cvd_3ago_col, cvd_4ago_col, cvd_5ago_col, cvd_6ago_col])
cvd_df_au = cvd_df[cvc_df["Country/Region"].str.contains("Australia")]

# Add up the numerical columns
cvd_sums = cvd_df_au.sum(axis=0, numeric_only=True)

# Find latest death total
cvd_today = int(round(cvd_sums.iloc[6]))

##
# Display the data
##

infected_diff = cv_today - cv_1ago
# Uncomment to check data is being pulled properly
#print("\n\n\nAustralia Breakdown")
#print("-------------------")
#print(cvc_df_au)

output1 = str(cv_today) + " infected so far. (+" + str(infected_diff) + ")"
output2 = str(cvr_today) + " have recovered."
output3 = str(cvd_today) + " Australians have died."

# Graph the trend and save as image file
plt.plot(cv_sums, label="Infected", color="black")
plt.plot(cvr_sums, label="Recovered", color="green")
plt.plot(cvd_sums, label="Deaths", color="red")
plt.legend()
#plt.show()
plt.savefig('graph.png')
# TODO: Convert PNG to BMP for epd to display

##
# E-Paper Display
##

try:
    logging.info("loading coronagotchi")
    
    epd = epd2in13bc.EPD()
    logging.info("initialising and clearing display")
    epd.init()
    epd.Clear()
    time.sleep(1)
    
    # Drawing on the image
    logging.info("loading fonts")    
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
    
    # Drawing on the Horizontal image
    logging.info("writing to display") 
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)
    drawblack.text((10, 10), output1, font = font16, fill = 0)
    drawblack.text((10, 30), output2, font = font16, fill = 0)
    drawblack.line((10, 60, 230, 60), fill = 0)
    drawblack.text((10, 70), output3, font = font16, fill = 0)
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)
    
    #logging.info("3.read bmp file")
    #HBlackimage = Image.open(os.path.join(picdir, '2in13bc-b.bmp'))
    #HRYimage = Image.open(os.path.join(picdir, '2in13bc-ry.bmp'))
    #epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    #time.sleep(2)
    
    #logging.info("4.read bmp file on window")
    #blackimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    #redimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126    
    #newimage = Image.open(os.path.join(picdir, '100x100.bmp'))
    #blackimage1.paste(newimage, (10,10))    
    #epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))
    
    #logging.info("clearing display")
    #epd.init()
    #epd.Clear()
    
    logging.info("going to sleep")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13bc.epdconfig.module_exit()
    exit()