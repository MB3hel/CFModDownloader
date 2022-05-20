#
# Copyright 2022 Marcus Behel
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, 
# this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
# THE POSSIBILITY OF SUCH DAMAGE.
#


from email.mime import base
import platform
from re import L
import shutil
import tempfile
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import argparse
from typing import Dict, List
from pathlib import Path
import time
from enum import Enum, auto
from bs4 import BeautifulSoup



class Browser(Enum):
    Chrome = auto()
    Firefox = auto()


## Parser to get project ID from mod curseforge page.
class ModParser:

    ## Create parser.
    #  @param urls Specify a set of urls for mods to download
    #  @param browser Specify which browser to download mods with
    def __init__(self, urls, browser: Browser = Browser.Chrome):
        self.browser: Browser = browser
        self.urls: List[str] = urls
        self.num_threads = 4
        self.parse_lock = threading.Lock()      # used as much to synch prints as anything else
        self.parse_count = 0
        self.thread_results = []
        self.parse_urls = []
    

    ## Parse the URLs pages to find project IDs. Returns map of ID: url
    def parse(self) -> Dict[int, str]:
        # Start self.num_threads threads each managing its own browse window
        self.thread_results.clear()
        threads: List[threading.Thread] = []
        drivers: List[webdriver.Remote] = []
        self.parse_urls = self.urls.copy()
        for i in range(self.num_threads):
            d = self.__make_driver()
            t = threading.Thread(daemon=True, target=self.__thread_parse, args=(d,))
            t.start()
            threads.append(t)
            drivers.append(d)

        # Wait for all threads to finish & close browsers when done
        for i in range(self.num_threads):
            threads[i].join()
            drivers[i].quit()
        
        # Collect results into one dict
        data = {}
        for i in range(self.num_threads):
            data.update(self.thread_results[i])

        print("Done obtaining IDs.")

        return data

    def __thread_parse(self, driver: webdriver.Remote):
        data: Dict[int, str] = {}
        while True:        
            # Load and parse each page
            with self.parse_lock:
                if len(self.parse_urls) == 0:
                    break
                url = self.parse_urls.pop()
                print("Obtaining ID {0} of {1}...".format(self.parse_count, len(self.urls)))
                self.parse_count = self.parse_count + 1
            driver.get(url)
            soup = BeautifulSoup(driver.page_source)
            for span in soup.find_all("span"):
                if span.text.lower() == "project id":
                    sibling = span.find_next_sibling("span")
                    try:
                        data[int(sibling.text)] = url
                    except:
                        data[-1] = url
        self.thread_results.append(data)

    def __make_driver(self) -> webdriver.Remote:
        if self.browser == Browser.Chrome:
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif self.browser == Browser.Firefox:
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        else:
            raise Exception("Invalid browser")
