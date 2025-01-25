import csv
import requests
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("PRODUCTION_CLIENTID")
client_secret = os.getenv("PRODUCTION_CLIENTSECRET")



access_token = None

def get_access_token():
    url = "https://api.digikey.com/v1/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    data = {"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}

    at_result = requests.post(url, data=data, headers=headers)
    at_json = at_result.json()
    
    print("got access token")
    return at_json['access_token']




def get_product_pricing(stock_code):
    print(stock_code)
    print(client_id)
    print(access_token)
    url = "https://api.digikey.com/products/v4/search/" + stock_code + "/productdetails"
    headers = {"X-DIGIKEY-Client-Id": client_id, "Authorization": "Bearer " + access_token}

    pp_result = requests.get(url, headers=headers)
    pp_json = pp_result.json()

    print(pp_json)
# def get_product_pricing(stock_code):


# with open('Bill Of Materials PowerPortMax-v5.csv', newline='') as csvfile:

#     bomreader = csv.reader(csvfile, delimiter=' ')

#     for row in bomreader:
#         print(row)

access_token = get_access_token()
print("Assigned access token:" + access_token)

get_product_pricing("RC0402FR-07953RL")
    