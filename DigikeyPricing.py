import csv
import requests
from dotenv import load_dotenv
import os

load_dotenv()



def get_access_token():

    load_dotenv()

    client_id = os.getenv("CLIENTID")
    client_secret = os.getenv("CLIENTSECRET")

    url = "https://sandbox-api.digikey.com/v1/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    data = {"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}

    at_result = requests.post(url, data=data, headers=headers)
    at_json = at_result.json()

    return at_json['access_token']

# def get_product_pricing(stock_code):


# with open('Bill Of Materials PowerPortMax-v5.csv', newline='') as csvfile:

#     bomreader = csv.reader(csvfile, delimiter=' ')

#     for row in bomreader:
#         print(row)

get_access_token()
    