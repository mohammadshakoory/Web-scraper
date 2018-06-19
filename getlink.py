#Author: Mohammad Shakoory
#Date : 5/26/2018

import requests
import urllib
from bs4 import BeautifulSoup

#this function gets the links to each solar farm specific page
def get_info_page_link():
    print "First Stage"
    result = []
    solar_page = requests.get("http://dg.nyserda.ny.gov/facilities/index.cfm?sort=Output&order=DESC&Filter=Solar")
    soup = BeautifulSoup(solar_page.content, 'html.parser')
    table = soup.find_all('table')
    distable = table[2].find_all('table')
    solartable = distable[2].find_all('tr')

    for lnk in solartable[1:]:
        result.append("http://dg.nyserda.ny.gov/facilities/" +lnk.find('a')["href"])
    return result

#this function gets the links to the csv download page
def link_to_csv_init(links):
    print "Second Stage"
    res_link = []
    for url in links:
        csv_init = requests.get(url)
        soup = BeautifulSoup(csv_init.content, 'html.parser')
        linkss = soup.find_all('div', {"class": "InfoData"})
        csv = linkss[2].find_all('a')
        if len(csv) > 1:
            res_link.append("http://dg.nyserda.ny.gov/"+csv[1]["href"])


    return res_link

#this function gets the unit number of each solar farm to be concatinated to a url
def get_unit(urls):
    print "Third Stage"
    temp = []
    result = []

    for url in urls:
        temp.append(url[::-1])

    for rev in temp:
        rev_unit = ''
        for c in rev:
            if c == "=":
                break
            else:
                rev_unit += c
        result.append(rev_unit[::-1])
    return result

#this function recieves the unit number and POSTs form data to the website to recieve a link which could is downloadeable
def download_csv(unit):
    print "Fourth Stage"
    params = {"StartDate": "04/01/2018", "EndDate": "05/31/2018", "Interval": "Hourly", "Unit": unit, "Type": "csv"}
    r = requests.post("http://dg.nyserda.ny.gov/reports/csvreport.cfm", data=params)
    doc = BeautifulSoup(r.text, 'html.parser')
    a_tag = doc.find_all('a', {"target": "_blank"})
    if len(a_tag) > 0:
        urllib.urlretrieve(a_tag[0]["href"], unit+".csv")

#this function integrates all parts of the process
def integration():
    print "initiation"
    res = get_info_page_link()
    ll = link_to_csv_init(res)
    units = get_unit(ll)
    for unit in units:
        download_csv(unit)

if __name__ == "__main__":

    integration()

