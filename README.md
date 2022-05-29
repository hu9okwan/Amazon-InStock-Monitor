# Amazon-InStock-Monitor 📈
This script monitors the availability status of an Amazon product by scraping information from it's product page. It will then send a notification sound alert if either the price, availability, or the "See Buying Options" button are present and returns a result.

## Usage
1. Install required modules
2. Update `main("enter url here", 60)` with the URL of the product and change 60 to desired check interval in seconds
3. If using proxies:
    - Create `proxies.csv` in the same script location
    - Enter proxies on every new line in the format of IP:Port `192.168.1.254:8080`
5. Run `& C:/Python38/python.exe path/to/script/amztracker.py`
