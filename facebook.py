# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 01:57:06 2021

@author: wenchen
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


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

def get_all_post(num):
    posts = []
    while(len(posts) < num):
        # rolling page
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        # find post blcok
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
        content_ = ""
    return content_


def get_img_content(post):
    try:
        img_content_ = post.find("img")["alt"]
    except:
        img_content_ = ""
    return img_content_

def post_decode(posts, author, content, img_content):
    info_list = []

    for post in posts:
        
        sub_list = []
        # get uesr/club name
        if(author):
            sub_list.append(get_author(post))
        
        #get content
        if(content):
            sub_list.append(get_content(post))
        
        #get img title
        if(img_content):
            sub_list.append(get_img_content(post))
        
        info_list.append(sub_list)
        
    return info_list





if __name__ == '__main__':
    usr = "YOUR EMAIL"
    password_filename = 'mypass.txt'
    chrome = connect_and_login(usr, password_filename)
    posts = get_all_post(num=20)
    info_list = post_decode(posts, author=True, content=True, img_content=True)
    print(info_list)


