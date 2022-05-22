from bs4 import BeautifulSoup
import requests
import time
import playsound
import webbrowser


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



def main(url):

    # user agents
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    
    count = 1
    opened = False
    while True:

        # get request for page data
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
        available_stock_terms = ["In Stock.", "Only 2 left in stock.", "Only 1 left in stock."]
        if price or buying_options or avail in available_stock_terms:
            playsound.playsound("alert.mp3")
            if not opened:
                webbrowser.open(url)
                opened = True

        count +=1
        time.sleep(60)


if __name__ == '__main__':

    main("enter url here")

