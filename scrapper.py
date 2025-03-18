# app.py
from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
import csv
import datetime

app = Flask(__name__)

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        product_name = request.form['product_name']
        data = check_price(product_name)
        return render_template('results.html', data=data)

def check_price(product_name):
    URL = f'https://www.amazon.com/s?k={product_name}&ref=nav_bb_sb'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }

    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")

    products = soup1.find_all('div', {'data-component-type': 's-search-result'})

    data = []
    for product in products:
        try:
            # title = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).get_text().strip()
            title = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).get_text().strip()
            email_element = product.find('span', {'class': 'a-size-base po-break-word'})
            email = email_element.get_text().strip() if email_element else 'info@amazon.com'
            image_url = product.find('img', {'class': 's-image'})['src']
            ratings_element = product.find('span', {'class': 'a-icon-alt'})  # Assuming ratings are represented as stars
            ratings = ratings_element.get_text().strip() if ratings_element else 'N/A'
            c1 = product.find('div', {'class': 'a-row a-size-base a-color-secondary'})
            c2 = c1.find('span', {'class': 'a-color-base'})
            price = c2.get_text().strip()
            price = price.replace('$', '').replace(',', '')
            price = float(price)
            commission = price * 0.1
            total_price = price + commission
            data.append({'Title': title, 'Price': price, 'Commission': commission, 'Total Price': total_price, 'Image URL': image_url, 'Ratings': ratings, 'Email': email})
        except AttributeError:
            pass

    return data

if __name__ == '__main__':
    app.run(debug=True)
