############################################################################
# copy right : https://github.com/june5079/soFrida/blob/master/getapklist.py

############################################################################

import requests
import time, sys
import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from pathos.multiprocessing import ProcessingPool
#from tqdm import tqdm
import platform

DRIVER_PATH = "/mnt/c/Users/k1rha/Desktop/Tools/chromedriver.exe"
# HOW to Use 
'''
from get_apk_list import Getlists
getlist = Getlists("basic", "happylabs") 
getlist.init_request()
getlist.get_result()
'''

class Getlists:

    def __init__(self):
        # Define base info
        self.play_search_basic = "https://play.google.com/store/search?q="
        self.play_search_pkgid = "https://play.google.com/store/apps/details?id="
        self.play_search_devid = "https://play.google.com/store/apps/dev?id="
        self.apklist = []
        self.result = dict()
        self.finished = False
        self.namespace = "/apk_download"
        self.proxy = {}

    def show_apk_list(self):
        return self.apklist

    def set_proxy(self, proxy):
        self.proxy = proxy

    def init_request(self, option, search_keyword, country):
        self.option = option
        self.search_keyword = search_keyword
        self.country = country
        
        if self.option == "basic" :
            self.request_url = self.play_search_basic + self.search_keyword + "&c=apps"
            print ("[+]self.reqeuset_url: "+self.request_url)
        elif self.option == "pkgid" :
            self.request_url = self.play_search_pkgid + self.search_keyword
            self.apklist = [search_keyword]
        elif self.option == "devid" :
            self.request_url = self.play_search_devid + self.search_keyword
        else :
            print ("Wrong categories")
            exit()

        # According to paystore version up, country code doesn't work anymore....  - k1rh4 - 
        #self.request_url+="&gl="+self.country

        print ("[+] self.request_url: "+self.request_url)
        if platform.system() == "Windows":
	        self.chrome_driver = DRIVER_PATH
        else:
	        self.chrome_driver = DRIVER_PATH
            #self.chrome_driver = "./chromedriver"
        if self.option == "pkgid":
            return 
            # self.f = open ("apklist_{0}.txt".format(self.search_keyword),"w")
        
        self.options = Options()    
        self.options.add_argument("--start-maximized")
        self.options.headless = True
        self.browser = webdriver.Chrome(self.chrome_driver, chrome_options=self.options)
        self.browser.maximize_window()
        self.make_connection()

    def make_connection(self):
        print("[+] set request_url : %s" %(self.request_url))
        self.browser.get(self.request_url)
        # Get Pkg names
        self.load_pkglists()

        # Call Parser
        self.full_source = self.browser.page_source
        self.parse_pkgnames()
    
    def parse_pkgnames(self):
        self.s = set()  
        soup = BeautifulSoup(self.full_source, "html.parser")
        for link in soup("a"):
            if 'href' in link.attrs:
                self.s.add(link.attrs['href'])
        for x in self.s:
            if "details?id" in x:
                self.apklist.append(x.split("=")[1])
                #print("[+] package name : " + repr(self.apklist))
        # self.f.close()
        print ("[+] Success getting package name. ")
        print ("[+] Done Grabbing APK Lists.")
        #print (repr(self.apklist))
        self.browser.close()
        time.sleep(2)                

    def click_more(self):
        try:
            self.browser.find_element_by_css_selector("#show-more-button").click()
            self.load_pkglists()
        except:
            print ("Done")
            pass

    def load_pkglists(self):
        print("[+] {}".format("load package via scrolling"))
        self.reslist = []
        for _ in range(0, 5):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        self.click_more()

    def downfile_check(self, package_name):
        if (os.access("./apk",os.R_OK)):
            os.mkdir("./apk")

        return os.path.exists(os.path.join("./apk/") + package_name + '.apk')

    ## This method is not neeed just donwload apk... 
    def get_pkginfo(self):
        l = self.apklist
        i = 1
        for x in l:
            try:
                r = requests.get(self.play_search_pkgid + x.strip("\n"), proxies=self.proxy)
                res = r.text

                soup = BeautifulSoup(res, "html.parser" )

                pop = (soup.select ('div[class=IQ1z0d]'))[2]
                pop_cat = (soup.select ('span > a'))
                pop_title = (soup.select('h1 > span'))

                
                fin=''.join(str(e) for e in pop)  
                fin_pop = fin.split('+')[0].split('>')[1]
                
                fin_cat=''.join(str(k) for k in pop_cat)  
                fin_cat2 = fin_cat.split("category/")[1].split('"')[0]

                fin_title=''.join(str(g) for g in pop_title)
                fin_title2 = fin_title.split('>')[1].split('<')[0] 

                self.result[x]={"popular":fin_pop, "category":fin_cat2, "title":fin_title2}
                if self.downfile_check(x):
                    self.result[x]['status'] = "YES"
                else:
                    self.result[x]['status'] = "NO"

                print(repr(self.result))
            except Exception as e:
                print(e)
            i+=1
        time.sleep(0.5)

    ## This method is not neeed just donwload apk... 
    def get_pkginfo_for_socket_io(self):
        l = self.apklist
        i = 1
        for x in l:
            try:
                r = requests.get(self.play_search_pkgid + x.strip("\n"), proxies=self.proxy)
                res = r.text

                soup = BeautifulSoup(res, "html.parser" )

                pop = (soup.select ('div[class=IQ1z0d]'))[2]
                pop_cat = (soup.select ('span > a'))
                pop_title = (soup.select('h1 > span'))

                
                fin=''.join(str(e) for e in pop)  
                fin_pop = fin.split('+')[0].split('>')[1]
                
                fin_cat=''.join(str(k) for k in pop_cat)  
                fin_cat2 = fin_cat.split("category/")[1].split('"')[0]

                fin_title=''.join(str(g) for g in pop_title)
                fin_title2 = fin_title.split('>')[1].split('<')[0] 

                self.result[x]={"popular":fin_pop, "category":fin_cat2, "title":fin_title2}
                self.result[x]['status'] = os.path.exists(os.path.join("./apk/") + x + '.apk')
                print(repr(self.result))

            except Exception as e:
                print (e)
            i+=1
        self.finished = True
