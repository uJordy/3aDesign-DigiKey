import csv
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

def get_access_token(client_id, client_secret):
    url = "https://api.digikey.com/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "charset": "utf-8", "Accept": "application/json"}

    data = {"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["access_token"]
    else:
        print(f"Error retrieving access token \n Status Code: {response.status_code} Response Text:{response.text}")
        return None


# def get_product_price(product_data):
    

def get_product_pricing(stock_code):
    # print(stock_code)
    # print(client_id)
    # print(access_token)
    url = "https://api.digikey.com/products/v4/search/" + stock_code + "/pricing"
    headers = {"X-DIGIKEY-Client-Id": client_id, "Authorization": "Bearer " + access_token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        return response_json
    # elif response.status_code == 404:
    #     print("could not find product!")
    #     return None
    else:
        print(f"Error retrieving product price\n Status Code: {response.status_code} Response Text:{response.text}")
        return None
    

def calculate_product_price(stock_code,quantity):
    url = "https://api.digikey.com/products/v4/search/" + stock_code + "/digireelpricing?requestedQuantity=" + quantity
    headers = {"X-DIGIKEY-Client-Id": client_id, "Authorization": "Bearer " + access_token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        return response_json
    # elif response.status_code == 404:
    #     print("could not find product!")
    #     return None
    else:
        print(f"Error retrieving product price\n Status Code: {response.status_code} Response Text:{response.text}")
        return None

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

def init():

    with open("Bill Of Materials PowerPortMax-v5.csv", newline="") as csvfile:

        bomreader = csv.reader(csvfile)
        next(bomreader, None) # Skips header

        for row in bomreader:
            # print(row)
            # try:

            # print((row[4]))
            response = get_product_pricing(row[4])

            if type(res) != None:
                res
            else:
                print("None found!")


access_token = get_access_token(client_id, client_secret)
# init()


# print(get_product_pricing("RC0402FR-07953RL"))
# print(get_product_pricing("CSRF1206FT10L0"))
# print(get_product_pricing("74HC4067PW-Q100J"))

print(calculate_product_price("RC0402FR-07953RL","50"))
# print(get_product_pricing("nf"))

    