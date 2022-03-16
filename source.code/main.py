from pypresence import Presence
import configparser
import time
import requests
from pathlib import Path
from configparser import ConfigParser
from bs4 import BeautifulSoup
import requests
import re

# Validate Files #
path_to_file = 'config.ini'
path = Path(path_to_file)

if path.is_file():
    print("config.ini >> true - FILE EXISTS")
else:
    config_object = ConfigParser()
    config_object["profile"] = {
        "steam_link": "https://steamcommunity.com/id/0000000000000000"
        }
    with open('config.ini', 'w') as conf:
        config_object.write(conf)

# CLIENT INFO #
client_id = '953505733297709116'  # Client ID [DO NOT CHANGE]
RPC = Presence(client_id)  # Initialize the client class
RPC.connect() # Start the handshake loop

# CONFIG INFO #
config = configparser.ConfigParser()
config.read('config.ini')

steam_link_data = config['profile']['steam_link']
steam_link_str = str(steam_link_data)

# GET JOIN LINK #
def getHTMLdocument(url):
      
    # request for HTML document of given url
    response = requests.get(url)
      
    # response will be provided in JSON format
    return response.text
  
    
# assign required credentials
# assign URL
url_to_scrape = steam_link_str
  
# create document
html_document = getHTMLdocument(url_to_scrape)
  
# create soap object
soup = BeautifulSoup(html_document, 'html.parser')
  
  
# find all the anchor tags with "href" 
# attribute starting with "steam://"
for link in soup.find_all('a', 
                          attrs={'href': re.compile("^steam://")}):
    # display the actual urls
    join_link_get = link.get('href')
    join_link_str = str(join_link_get)

try:
    print(RPC.update(state="Playing In A Squad", details="in a lobby (NULL of NULL)", large_image = "logo_28", large_text="Ready or Not", buttons = [{"label": "Join Squad", "url": join_link_str}, {"label": "View Page", "url": "https://github.com/Zurek0x/Ready_Or_Not_Better-Presence"}]))  # Set the presence
except:
    print("[!] An error has occured!")
    print("[!] Check the profile link in (config.ini) and set it to your profile link!")
    print("[+] Current Link: " + steam_link_str)
    input("[>] Press Enter To Continue.")
    exit()

while True:
    time.sleep(5)
