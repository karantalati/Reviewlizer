#!/usr/bin/env python
# coding: utf-8

# # Amazon Product Review Scraper 

# In[1]:


import requests
from bs4 import BeautifulSoup


# In[2]:


product_url = input('Enter product url :')
product_url


# In[14]:


header={'User-Agent': 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}


# In[18]:


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
  
search_response=requests.get(product_url,headers=HEADERS)


# In[19]:


if search_response.status_code == 200:
    pass
else:
    print('Check your query')


# In[20]:


search_response.text   #prints the text part of response


# #### Fetching product name which will be later used to save CSV with same name

# In[49]:


soup = BeautifulSoup(search_response.content)

product_name = soup.find('span',{'id':'productTitle'}).text.strip()
product_name


# #### A function to pass on the link of 'see all reviews' and extract the content

# In[50]:


cookie = {}
def Searchreviews(review_link):
    url="https://www.amazon.com"+review_link
    print('scraping from :',url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# ##### By passing the url, we can extract the 'see all reviews' link for any product in the page

# In[51]:


link = []
soup=BeautifulSoup(search_response.content)
z = soup.find("a",{'data-hook':"see-all-reviews-link-foot"})
link = z['href']
link


# ##### Now we have the 'see all review' link. Using this link along with a page number, we can extract the reviews in any number of pages

# In[53]:


reviews_details=[]
for k in range(5):
    response=Searchreviews(link+'&pageNumber='+str(k))
    soup=BeautifulSoup(search_response.content)
    for i in soup.findAll("div",{'data-hook':"review"}):
#         y = soup.find('a',{'class':'a-link-normal'})
        name = (i.find('span',{'class':"a-profile-name"}).text)
        stars = (i.find('a',{'class':"a-link-normal"}).text)
        review = (i.find("span",{'data-hook':"review-body"}).text)
        reviews_details.append([name,stars,review])
        print('done....')


# In[54]:


import re
def cleanData(data):
    '''Removes all the leading, trailing whitespaces, 
    newline characters, emojis , special symbols etc and returns a clean list'''
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"  #misc.
        u"\U00002600-\U000027BF"                     
        u"\U000024C2-\U0001F251"
        u"\U0001f913-\U0001f937"
        u"\U0001f900-\U0001f9ff"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
    
    for row in data:
        row[0] = emoji_pattern.sub(r'', row[0]).strip()
        row[2] = emoji_pattern.sub(r'', row[2]).strip() #row[2]  ----> contains 'review' string
        
    return data
    


# In[55]:


import pandas as pd


# In[56]:


len(reviews_details)


# In[57]:


cleaned_data = cleanData(reviews_details)


# In[58]:


review_data=pd.DataFrame(reviews_details, columns = ['Name' , 'Rating', 'Review']) #converting list of list into a DF


# In[59]:


# print(reviews)
pd.set_option('max_colwidth',500)
review_data


# In[60]:


review_data.shape # (m,n) ---> m rows, n colums


# In[65]:


product_name = product_name.replace(":", "-   ") #windows does not allow ':' in file name
#converting the dataframe to a csv file so as to use it later for further analysis
review_data.to_csv("./Data603/" +product_name + '.csv', index = False)


# ##### references: 1)https://medium.com/analytics-vidhya/web-scraping-amazon-reviews-a36bdb38b257
# #####                     2)https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# In[ ]:




