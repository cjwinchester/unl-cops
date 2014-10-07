from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
import time

f = open('unlcrimes.txt', 'wb')

driver = webdriver.Chrome()
driver.get("https://scsapps.unl.edu/policereports/MainPage.aspx")

assert "Daily Crime" in driver.title

print "Connected!"

element = driver.find_element_by_name("ctl00$ContentPlaceHolder1$DateRange")

all_options = element.find_elements_by_tag_name("option")
for option in all_options:
    if option.get_attribute("value") == "month":
        option.click()
        time.sleep(5)
 
months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
years = ["2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014"]

for year in years:
    yearmenu = Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_YearSelection"))
    yearmenu.select_by_value(year)
    time.sleep(10)
    for month in months:
        monthmenu = Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_MonthSelection"))
        monthmenu.select_by_value(month)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source)
        for linebreak in soup.findAll('br'):
            linebreak.extract()
        table = soup.find('table', {'style': 'padding: 10px'})
        for row in table.findAll('tr'):
            col = row.findAll('td')
            incident_no = col[0].a.renderContents().strip()
            print incident_no
            f.write(incident_no + "|")
            things = row.find_all('span', id=re.compile("^ctl00_ContentPlaceHolder1_Results"))
            for thing in things:
                f.write(thing.renderContents().strip().replace('<span style="font-weight:bold;">','').replace('</span>','') + "|")
            f.write('\n')
    time.sleep(10)

f.flush()
f.close()        
driver.close()
