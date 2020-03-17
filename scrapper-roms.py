import requests, bs4, json, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def getDownloadLink(titulo, link):
  driver = webdriver.Firefox()
  driver.implicitly_wait(30)
  driver.get(link)
  button = driver.find_element_by_class_name('acf-get-content-button')[0];
  button.click();


 



getDownloadLink('bla', 'https://cdromance.com/ps2-iso/speed-racer-europe/')

resallroms = requests.get('https://cdromance.com/ps2-iso/');
resallroms.raise_for_status();

soup = bs4.BeautifulSoup(resallroms.text, "html.parser");
rows = soup.select('.games-listing-table > tbody > tr ')


