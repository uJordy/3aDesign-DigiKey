# Name: DigikeyPricing.py
# Author: too small to credit
# Description: Iterates through a specific CSV file to generate a Bill of Materials (BOM) for a requested quantity
# Usage: Use the command terminal to run the folliowing command:
#   # DigikeyPricing.py "Bill Of Materials PowerPortMax-v5.csv"  50

#  Args[1] = CSV file
#  Args[2] = Quantity

import csv
import sys
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

client_id = os.getenv("PRODUCTION_CLIENTID")
client_secret = os.getenv("PRODUCTION_CLIENTSECRET")

# client_id = os.getenv("CLIENTID")
# client_secret = os.getenv("CLIENTSECRET")

access_token = None
requested_quantity = None
csvdict = []
output_filename = "BOM Results.csv"


def get_access_token(client_id, client_secret):
    url = "https://api.digikey.com/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["access_token"]
    else:
        print(f"Error retrieving access token \n Status Code: {response.status_code} Response Text:{response.text}")
        return None

    

def get_product_pricing(stock_code):
    url = "https://api.digikey.com/products/v4/search/" + stock_code + "/pricing?limit=1"
    headers = {"X-DIGIKEY-Client-Id": client_id, "Authorization": "Bearer " + access_token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        print(f"Error retrieving product prices\n Status Code: {response.status_code} Response Text:{response.text}")
        return None


# product_details needs to be the response json of get_product_pricing
def get_lowest_product_price(product_details, quantity):
    quantity = int(quantity)
    lowest_price_details = None

    if not "ProductPricings" in product_details:
        print("Invalid parameter for get_lowest_product_price")
        return None
    else:
        for p_variations in product_details["ProductPricings"][0]["ProductVariations"]:
            for break_price in p_variations["StandardPricing"]:
  
                if not lowest_price_details: # if no lowest price defined, declare it so it can be compared with other break prices
                    lowest_price_details = break_price
                elif quantity >= break_price["BreakQuantity"] and break_price["UnitPrice"] < lowest_price_details["UnitPrice"]: #check if quantity is bigger than the break price quantity and that its cheaper
                    lowest_price_details = break_price

        return lowest_price_details


# INDEX KEYS  #

# 0 = Category
# 1 = Quantity
# 2 = Reference
# 3 = Value
# 4 = Stock Code
# 5 = Description
# 6 = Unit Cost
# 7 = PCB Package
# 8 = Manufacturer

def add_csv_entry(stock_code, quantity, break_quantity, unit_price, total_price):
    csventry = {"Stock Code": stock_code, "Requested Quantity": quantity, "Batch Size": break_quantity, "Unit Price": unit_price, "Total Price": total_price}
    csvdict.append(csventry)

def create_output_csv(headers, csvdict):
    with open(output_filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(csvdict)

def init():

    filename = sys.argv[1]
    requested_quantity = sys.argv[2]

    with open(filename, newline="") as csvfile:

        bomreader = csv.reader(csvfile)
        next(bomreader, None) # Skips header

        print("Starting loop")
        for row in bomreader:

            stock_code = row[4]
            product_details = get_product_pricing(stock_code)
            
            # Sanity Checks
            if product_details == None:
                add_csv_entry(stock_code, "", "", "", "")
                print(f"No product details found for: {stock_code}")
                continue 
            if product_details["ProductsCount"] == 0:
                add_csv_entry(stock_code, "", "", "", "")
                print(f"No product details found for: {stock_code}")
                continue 
            

            lowest_price_details = get_lowest_product_price(product_details, requested_quantity)

            unit_price = lowest_price_details["UnitPrice"]
            total_price = float(unit_price) * float(requested_quantity)
            


            add_csv_entry(stock_code, requested_quantity, lowest_price_details['BreakQuantity'], unit_price, total_price)
        
        create_output_csv(["Stock Code", "Requested Quantity", "Batch Size", "Unit Price", "Total Price"], csvdict)
        print(f"Finished. See CSV file {output_filename} in local directory")


access_token = get_access_token(client_id, client_secret)
init()



    