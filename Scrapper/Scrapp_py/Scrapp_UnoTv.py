#!/usr/bin/env python
# coding: utf-8

# In[1]:


SEED_CRAWL = 'https://json.unotv.com/search?q=&res_start=0'


# In[2]:


import random
import requests
from requests_html import HTMLSession
from requests_html import HTML
import os
import json
import validators


# In[3]:


class Crawler:
    
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]



    all_json_to_send = []
    
    
    def _init_(self):
        pass
    
    
    def start_request(self,url):
        session = HTMLSession()
        header = dict()
        header['user-agent'] = random.choice(self.USER_AGENT_LIST)
        response = session.get(url,headers=header)        
        return response
    
    
    def parse(self, response):
        self.all_json_to_send = []
        json_data = json.loads(response.html.html)["listaResultados"]
        for url_data in json_data:
            json_to_send = {}
            json_to_send["url"] = url_data["url_nota"]
            self.all_json_to_send.append(json_to_send)


# In[4]:


crawler = Crawler()

response = crawler.start_request(SEED_CRAWL)


# In[5]:


response.html.html


# In[6]:


crawler.parse(response)


# In[7]:


crawler.all_json_to_send


# In[8]:


assert(len(crawler.all_json_to_send)>0)


# In[9]:


assert validators.url(crawler.all_json_to_send[0]["url"])


# In[10]:


SEED_SCRAP = 'https://www.unotv.com/internacional/estados-unidos-exigira-prueba-covid-19-negativa-para-ingresar-en-avion/'


# In[11]:


QUERY_TITLE = "//h1[@class='entry-title']"
QUERY_CONTENT =  "//div[@class='entry-content']//*[self::p|self::h2|self::ul]"
QUERY_DATE = "//time[@class='entry-date published']/@datetime"


# In[12]:


import json
import w3lib.html
import random
import os
import datetime
import requests
import string
import calendar
import html
import locale 
import datefinder
from requests_html import HTMLSession
import re


# In[25]:


class Scraper:
    
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    query_extract_title = QUERY_TITLE
    query_extract_text =  QUERY_CONTENT
    query_extract_date = QUERY_DATE

    
    def _init_(self):
        pass

  
    def start_request(self,url):
        headers = {'user-agent':random.choice(self.USER_AGENT_LIST) }
        session = HTMLSession()
        response = session.get(url,headers=headers)  
        return response
    

    def clean_text(self, html_text):
        text_without_tags = w3lib.html.remove_tags(html_text)
        text_without_escape_chars = w3lib.html.replace_escape_chars(text_without_tags)
        text_without_escape_chars = html.unescape(text_without_escape_chars)
        text_without_whitespace = text_without_escape_chars.strip()
        return text_without_whitespace
    
    def replace_month_name_to_number(self,date_string):
        lower_string = date_string.lower()
        for month_id in range(1, 13):
            if(lower_string.find(calendar.month_name[month_id].lower())!=-1):
                if(month_id>=10):
                    return (lower_string.replace(calendar.month_name[month_id].lower(),str(month_id)))
                else:
                    return (lower_string.replace(calendar.month_name[month_id].lower(),"0"+str(month_id)))
            if(lower_string.find(calendar.month_abbr[month_id].lower())!=-1):
                if(month_id>=10):
                    return (lower_string.replace(calendar.month_abbr[month_id].lower(),str(month_id)))
                else:
                    return (lower_string.replace(calendar.month_abbr[month_id].lower(),"0"+str(month_id)))
                    

    def format_date(self,date):
        matches = datefinder.find_dates(date)
        for match in matches:
            return (match.strftime("%Y-%m-%d"))
        


    def parse(self, response):
        self.news_text = []
        self.message_to_send = []
        self.scraped_url = response.url
        self.news_title = response.html.xpath(self.query_extract_title)[0].text
        self.date = response.html.xpath(self.query_extract_date)[0]
        self.news_title = self.clean_text(self.news_title)
        self.date = self.clean_text(self.date)
        self.date = self.format_date(self.date)    
        news_text_extracted_response = response.html.xpath(self.query_extract_text)
        for part_of_body in news_text_extracted_response:
            stripped_html_tags = w3lib.html.remove_tags(part_of_body.text)
            text_cleaned = self.clean_text(stripped_html_tags)
            self.news_text.append(text_cleaned)
        self.news_text.pop()


# In[26]:


scraper = Scraper()
response =scraper.start_request(SEED_SCRAP)


# In[27]:


scraper.parse(response)


# In[28]:


scraper.news_title


# In[29]:


scraper.date


# In[30]:


scraper.news_text


# In[31]:


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except:
        print("La fecha no tiene el formato correcto, año-mes-dia")
        return False

    
def test_news_title_has_text(news_title):
    regex_string_only_numbers = r'^[0-9\.\ ]*$'
    news_text_is_only_number_query = re.match(regex_string_only_numbers,news_title)
    if(news_text_is_only_number_query is None):
        return True
    else:
        return False

    
def test_news_text_has_text(news_text):
    joined_text =   " ".join(news_text)
    regex_string_only_numbers = r'^[0-9\.\ ]*$'
    news_text_is_only_number_query = re.match(regex_string_only_numbers,joined_text)
    if(news_text_is_only_number_query is None):
        return True
    else:
        return False

        
def test_news_title_length(news_title):
    words_of_news_title = news_title.split(" ")
    len_of_each_news_title_word = list(map(len,words_of_news_title))
    avg_of_news_words = sum(len_of_each_news_title_word)/len(len_of_each_news_title_word)
    if(avg_of_news_words >= 1.5):
        return True
    else:
        return False

    
def test_news_text_length(news_text):
    len_of_each_news_text_words = []
    for paragraph in news_text:
        splited_words = paragraph.split(" ")
        len_of_each_news_text_words.extend(list(map(len,splited_words)))
    avg_of_news_words = sum(len_of_each_news_text_words)/len(len_of_each_news_text_words)
    if(avg_of_news_words >= 1.5):
        return True
    else:
        return False


# In[32]:


assert(len(scraper.news_title)>0)
assert(len(scraper.news_text)>0)
assert(validate(scraper.date))
assert(isinstance(scraper.news_title,str))
assert(isinstance(scraper.news_text,list)) 
assert(scraper.news_title.find("<script>")==-1)
assert(scraper.news_title.find("</script>")==-1)
for text_piece in scraper.news_text:
    assert(text_piece.find("<script>")==-1)
    assert(text_piece.find("</script>")==-1)
assert(test_news_title_has_text(scraper.news_title))
assert(test_news_text_has_text(scraper.news_text))
assert(test_news_title_length(scraper.news_title))
assert(test_news_text_length(scraper.news_text))


# In[ ]:




