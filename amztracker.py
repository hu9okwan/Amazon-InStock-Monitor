from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectTimeout, ProxyError
import time
import playsound
import webbrowser
import csv
from itertools import cycle


def get_proxy_list(file):
    # get proxy list from csv

    proxy_list = []
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            proxy_list.append(row[0])

    return proxy_list


def get_product_title(soup):
    # get product title

    try:
        title = soup.find("span", attrs={"id": 'productTitle'}).string.strip()
    except AttributeError:
        title = False

    return title


def get_product_price(soup):
    # get product price

    try:
        price = soup.find("input", attrs={'id': 'attach-base-product-price'})['value']
    except TypeError:
        price = False

    return price


def get_product_availabity(soup):
    # get availablility status

    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = False
        
    return available


def get_buying_options_btn(soup):
    # check if there is "See All Buying Options" button

    buying_options = soup.find("span", attrs={"id": 'buybox-see-all-buying-choices'})
    if buying_options:
        return True
    else:
        return False



def main(url, interval):

    # user agents
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    
    # initialize proxy pool to rotate through
    use_proxy = True
    try:
        proxy_list = get_proxy_list("proxies.csv")
        proxy_pool = cycle(proxy_list)

        if len(proxy_list) == 0:
            print("empty csv file; script will not be using proxies")
            use_proxy = False

    except FileNotFoundError:
        print("csv file not found; script will not be using proxies")
        use_proxy = False
    

    count = 1
    opened = False
    while True:

        if use_proxy:
            # get next unused proxy from the pool using round robin
            proxy = next(proxy_pool)

            # get request for page data
            try:
                data = requests.get(url, headers=HEADERS, proxies={"http": proxy, "https": proxy}, timeout=2)
            except (ConnectTimeout, ProxyError) as error:
                print(f"{type(error).__name__}: {proxy}")
                continue
        else:
            data = requests.get(url, headers=HEADERS)

        soup = BeautifulSoup(data.content, "lxml")


        # get product info
        title = get_product_title(soup)
        price = get_product_price(soup)
        avail = get_product_availabity(soup)
        buying_options = get_buying_options_btn(soup)

        # print results
        not_avail = "N/A"
        print(f"================================== Check {count}")
        print(f"Product title : {title if title else not_avail}")
        print(f"Product price : {price if price else not_avail}")
        print(f"Availability  : {avail if avail else not_avail}")
        print(f"Buying options: {buying_options if buying_options else not_avail}")

        # play alert sound if in stock
        avail_stock_terms = ["In Stock.", "Only 2 left in stock.", "Only 1 left in stock."]
        # avail_but_not_in_stock = ["Usually ships within 1 to 2 months.", "Temporarily out of stock."]
        if (price and "in stock" in avail) or buying_options or avail in avail_stock_terms:
            playsound.playsound("alert.mp3")
            if not opened:
                webbrowser.open(url)
                opened = True

        count +=1
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            print(f"================================== Script exited")
            quit()


if __name__ == '__main__':
    main("enter url here", 60)
