# all imports
from flask import Flask, request, render_template, session, redirect, jsonify # flask imports
import requests
import bs4
import pandas as pd
import numpy as np
from datetime import datetime
import json


app = Flask(__name__)   #start flask app

# urls and date
url = 'https://hamariweb.com/finance/forex/inter_bank_rates.aspx'
date = datetime.now().strftime('%Y %m %d')

#get webpage to parse
def get_webpage(url):

    response = requests.get(url)
    return bs4.BeautifulSoup(response.text, 'html.parser')

# scrape and parse
def scrape(webpage):
    rows = webpage.find_all("tr") # find all elements to display
    cy_data = []
    for row in rows:
        cells = row.find_all("td") 
        cells = cells[1:4]
        cy_data.append([cell.text for cell in cells]) # appe4nd data in data frame
    return pd.DataFrame(cy_data, columns=['Currency', 'Buying', 'Selling']).drop(0, axis=0)

# routing and display data on local server
@app.route('/', methods=("POST", "GET"))
def html_table():

    page = get_webpage(url)
    data = scrape(page)
    result = json.dumps(json.loads(data.groupby(['Currency']).
                        apply(lambda x:x [['Currency','Buying','Selling']]).
                        to_json(orient='records')), indent=4, sort_keys=True)
    return result # returns jsonified elements to display on server

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) # app running on port 5000