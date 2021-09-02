# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 01:57:06 2021

@author: wenchen
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html

def connect_and_login(usr, password_filename):
    #connertion
    options = Options()
    options.add_argument("--disable-notifications")
     
    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome.get("https://www.facebook.com/")
    
    
    email = chrome.find_element_by_id("email")
    password = chrome.find_element_by_id("pass")
    # read password from file
    with open(password_filename) as f:
        lines = f.readlines()
    my_password = lines
    email.send_keys(usr)
    password.send_keys(my_password)
    password.submit()
    # waiting login
    time.sleep(3)
    return chrome
def isclickable(e):
    try:
        WebDriverWait(chrome, 10).until(EC.element_to_be_clickable(e))
        return True
    except :
        return False

def get_all_post(chrome, num):
    posts = []
    while(len(posts) < num):
        # rolling page
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        tree = html.fromstring(chrome.page_source)
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        # click See more
        elements = chrome.find_elements(By.XPATH, "//*[text()='See more']")
        el = tree.xpath("//*[text()='See more']")
        
        for i in range(len(elements)):
            try:
                elements[i].click()
            except :
                if(el[i].getroottree().getpath(el[i])!="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div/div/div/span/span"):    
                    print("missed some content", el[i].getroottree().getpath(el[i]))

        posts = soup.find_all("div", class_ = "du4w35lb k4urcfbm l9j0dhe7 sjgh65i0") 
        
        time.sleep(5)
    return posts[:num]

def get_author(post):
    try:
        author_ = post.find("strong").text
    except:
        author_ = post.find("span").text
    return author_

def get_content(post):
    content_ = ""
    try:
        contents_ = post.find_all("div", class_ = "kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q")
        for c in contents_:
            content_ += c.text
    except:
        pass
    try:
        contents2_ = post.find_all("div", class_ = "o9v6fnle cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q")
        for c in contents2_:
            content_ += c.text
    except:
        pass
    return content_


def get_img_content(post):
    img_content_ = ""
    try:
        img_content_ = post.find("img")["alt"]
    except:
        pass
    try:
        img_content_ += post.find("span", class_ = "a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ojkyduve").text
    except:
        pass
    return img_content_

def get_like(post):
    like_num = ""
    try:
        like_num = post.find("span", class_ = "pcp91wgn").text
    except:
        pass
    return like_num

def post_decode(posts, author, content, img_content, like):
    info_list = []

    for post in posts:
        
        sub_list = []
        # get uesr/club name
        if(author):
            sub_list.append(get_author(post))
        
        #get content
        if(content):
            sub_list.append(get_content(post))
        
        # get img title/alt
        if(img_content):
            sub_list.append(get_img_content(post))
        # get number of like
        if(like):
            sub_list.append(get_like(post))
        
        info_list.append(sub_list)
        
    return info_list





if __name__ == '__main__':
    usr = "YOUR EMAIL"
    password_filename = 'mypass.txt'
    chrome = connect_and_login(usr, password_filename)
    posts = get_all_post(chrome, num=10)
    info_list = post_decode(posts, author=True, content=True, img_content=True, like=True)
    print(info_list)


