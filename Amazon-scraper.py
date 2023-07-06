import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize variables for optional fields
    product_description = ''
    asin = ''
    manufacturer = ''

    # Extract product description if available
    product_description_element = soup.find('div', {'id': 'productDescription'})
    if product_description_element:
        product_description = product_description_element.get_text(strip=True)

    # Extract ASIN if available
    asin_element = soup.find('th', string='ASIN')
    if asin_element:
        asin = asin_element.find_next_sibling('td').get_text(strip=True)

    # Extract manufacturer if available
    manufacturer_element = soup.find('th', string='Manufacturer')
    if manufacturer_element:
        manufacturer = manufacturer_element.find_next_sibling('td').get_text(strip=True)

    # Find all the product containers on the page
    product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})

    scraped_data = []

    for container in product_containers:
        product_url = container.find('a', {'class': 'a-link-normal'})['href']
        product_name = container.find('span', {'class': 'a-size-medium'}).text.strip()
        product_price = container.find('span', {'class': 'a-offscreen'}).text.strip()
        product_rating = container.find('span', {'class': 'a-icon-alt'}).text.strip()
        product_reviews = container.find('span', {'class': 'a-size-base'}).text.strip()

        product_data = {
            'URL': product_url,
            'Name': product_name,
            'Price': product_price,
            'Rating': product_rating,
            'Reviews': product_reviews,
            'Description': product_description,
            'ASIN': asin,
            'Product Description': product_description,
            'Manufacturer': manufacturer
        }

        scraped_data.append(product_data)

    return scraped_data


def scrape_multiple_pages(base_url, num_pages):
    all_data = []

    for page_num in range(1, num_pages + 1):
        url = base_url + '&page=' + str(page_num)
        page_data = scrape_page(url)
        all_data.extend(page_data)

    return all_data

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
num_pages = 20

scraped_data = scrape_multiple_pages(base_url, num_pages)

def save_to_csv(data, filename):
    fieldnames = ['URL', 'Name', 'Price', 'Rating', 'Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

save_to_csv(scraped_data, 'amazon_products.csv')
