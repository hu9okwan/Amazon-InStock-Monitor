# Amazon-InStock-Monitor 📈
This script monitors the availability status of an Amazon product by scraping information from its product page. A notification sound alert is played if the "In stock" line or the "See Buying Options" button are detected.

## Usage
1. Install required modules
2. Update `main("enter url here", 60)` with the URL of the product and change 60 to desired check interval in seconds. 
    - Note: Stay above 60 seconds as they may have anti-scraping measures if requests are sent too often
4. If using proxies:
    - Create `proxies.csv` in the same script location
    - Enter proxies on every new line in the format of IP:Port `192.168.1.254:8080`
5. Run `& C:/Python38/python.exe path/to/script/amztracker.py`
