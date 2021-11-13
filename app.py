#!/usr/local/bin/python3

import logging
import requests
import numpy as np
import argparse
import sys

base_url = "https://api.sandbox.gemini.com/"

def price(s):
  # current price of symbol

  # make the actual request to the api
  try:
    response = requests.get(base_url + "v1/pubticker/{0}".format(s)).json()
  except:
    logging.critical("Can't talk to gemini API")
    raise sys.exit()

  return float(response['ask'])

def get_candles(s, duration="1day"):
  # time-intervaled data for the provided symbol

  # make the actual request to the api
  try:
    return requests.get(base_url + "v2/candles/{0}/{1}".format(s,duration)).json()

  except:
    logging.critical("Can't talk to gemini API")

def pdev(s):
  # Price Deviation - Generate an alert if the current price is more than one standard deviation from the 24hr average

  # get data from the last 24hr
  candles_data = get_candles(s, duration="1day")

  try:
    all_closed_prices_from_duration = [ data[4]  for data in candles_data  ]

    # using the std method to get standard deviation,
    #
    # not sure if they wanted the Absolute mean deviation,  which we can get by df.mad() instead

    std = np.std(all_closed_prices_from_duration, ddof=1)

  except:
    logging.error('Parsing errror with price deviation function')

  else:
    if price > std:
      logging.warning('Price is higher than the standard deviation for symbol '+s)

def pchange(s, per):
    # Price Change - Generate an alert if the current price has changed in the past 24 hours by more than X% from the price at the start of the period

    # grab last row, 2d column for the open price
    try:
      last_open_price_from_range = candles_data[ len(candles_data) -1 ][1]
    except:
       logging.error('Parsing errror with price change function')

    if price > last_open_price_from_range:
      percentage = (last_open_price_from_range / price * 100)

      # If the price increase is higher than the percentage we define,  alert to STDOUT
      if percentage > per:
         logging.warning("Current price {0} is {1}%  higher than start of period {2}".format(price, percentage, last_open_price_from_range))


def volumechange(s, per):
   # Volume Deviation - Generate an alert if the quantity of the most recent trade is more than X% of the total 24hr volume in the symbol


   try:
       # get first row with volume info
       current_volume = candles_data[0][5]
       volume_sum = 0

       # sum up all volumes except first index
       [ volume_sum := volume_sum + volume[5] for volume in candles_data[1:] ]
   except:
        logging.error('Parsing errror with volume change function')

   if volume_sum > current_volume:
     percentage = (current_volume / volume_sum * 100)

     if percentage > per:
       logging.warning("Current volume {0} is {1}% of 24hr volumes".format(current_volume, percentage))

# entrypoint into program
if __name__ == '__main__':

   parser = argparse.ArgumentParser(description='Connect to Gemini with the following arguments')
   parser.add_argument('--symbol','-s', type=str, required=True, help='symbol to proccess, ie: btcusd')
   parser.add_argument('--type','-t', type=str, required=True, help='Call to make (pricedev,pricechange,voldev,all)')
   parser.add_argument('--percentage','-p', type=int, help='Input the percentage you want , ie, you want 25% input -p 25')

   args = parser.parse_args()

   # get candles data for last 24hrs
   candles_data = get_candles(args.symbol, duration="1day")
   # grabbing price and data before function calls to scale back on http requests
   price = price(args.symbol)

   # argparser is wierd with floats, so whatever is passed with -p will be converted to decimal
   percent = args.percentage * 0.01

   if args.type == "all":
     pdev(args.symbol)
     pchange(args.symbol, percent)
     volumechange(args.symbol, percent)

   elif args.type == "pricedev":
     pdev(args.symbol)

   elif args.type == "pricechange":
     pchange(args.symbol, percent)

   elif args.type == "voldev":
     volumechange(args.symbol, percent)

   else:
     logging.critical("Type unkown, please specify -t (pricedev,pricechange,voldev,all)")
