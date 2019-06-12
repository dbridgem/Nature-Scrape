# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 11:18:42 2019

This script will scrape the entirety of Nature's archives (takes about a day) and save
all published material, along with the date it was published and type of publication (opinion, letter, etc)
@author: Devon
"""

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time

#Parse to get data of interest from each page
def Parser(soup):
    article_names_raw = soup.find_all('h3',class_ = 'mb10 extra-tight-line-height word-wrap')
    article_types_raw = soup.find_all('p',class_ = 'mb4 text13 tighten-line-height text-gray-light')
    article_dates_raw = soup.find_all('time')
    
    article_name = pd.Series()
    article_type = pd.Series()
    article_date = pd.Series()
    for i in range(len(article_names_raw)):
        temp_name = (article_names_raw[i]).get_text()
        temp_articletype = (article_types_raw[i]).get_text()
        temp_date = (article_dates_raw[i]).get_text()
        
        startflag = 0
        
        for j in range(len(temp_name)):
            if temp_name[j] != ' ' and temp_name[j] != '\n':
                startflag += 1
            if startflag == 1:
                temp = temp_name[j:len(temp_name)-1]
                startflag += 1
        
        article_name = article_name.append(pd.Series(temp),ignore_index=True)
        article_type = article_type.append(pd.Series(temp_articletype),ignore_index=True)
        article_date = article_date.append(pd.Series(temp_date),ignore_index=True)
    
    return(article_name,article_type,article_date)

if __name__ == '__main__':

    #Create Variables to store data
    articlename = pd.Series()
    articledate = pd.Series()
    articletype = pd.Series()
    
    #Iterate over 8250 pages of nature archives       
    for i in range(8250):    
        starttime = time.time()
        url = 'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page=' + str(i+1)
        
        page = urllib.request.urlopen(url) # conntect to website
        
        soup = BeautifulSoup(page, 'html.parser')
        
        #Send output from Beatiful Soup into parser
        [page_articlename,page_articletype,page_articledate] = Parser(soup)
        
        #Append data
        articlename = articlename.append(page_articlename,ignore_index=True)
        articletype = articletype.append(page_articletype,ignore_index=True)
        articledate = articledate.append(page_articledate,ignore_index=True)
        
        #Put a delay to avoid annoying the host
        time.sleep(0.25)
        endtime = time.time()
        print('Iteration time: ',endtime - starttime)
     
    #Save data to csv for later processing
    data = pd.DataFrame(data = [articlename,articletype,articledate])
    data = data.T
    data.columns = ['Name','Type','Date']
    data.to_csv('Nature_Data.csv',index=False)
