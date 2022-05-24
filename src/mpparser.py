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
    def __init__(self, urls, browser: Browser = Browser.Chrome, headless: bool = False):
        self.browser: Browser = browser
        self.headless = headless
        self.urls: List[str] = urls
        self.num_tabs = 4
    

    ## Parse the URLs pages to find project IDs. Returns map of ID: url
    def parse(self) -> Dict[int, str]:
        # Create driver for selected browser
        print("Launching browser...")
        driver = self.__make_driver(self.headless)

        data: Dict[int, str] = {}
        parse_urls = self.urls.copy()

        count = 1
        while True:
            # Open new tab if fewer than max (and more urls to parse)
            while len(driver.window_handles) < self.num_tabs + 1 and len(parse_urls) > 0:
                # Open a new tab loading the next url
                print("Obtaining ID for mod {0} of {1}...".format(count, len(self.urls)))
                count = count + 1
                driver.switch_to.window(driver.window_handles[0])
                driver.switch_to.new_window("tab")
                time.sleep(0.01)
                driver.execute_script("window.open('{0}', '_self');".format(parse_urls.pop()))

            # Only the "keepalive" tab remains and no more parse urls. Done parsing
            if len(driver.window_handles) == 1 and len(parse_urls) == 0:
                break

            # For all tabs, check if loading done. If so parse and close the tab
            # Ignore first tab. It just sits empty to ensure the browser does not close
            for win in driver.window_handles[1:]:
                # Select correct tab
                driver.switch_to.window(win)

                # Page is considered loaded when text "Project ID" is found
                try:
                    if driver.page_source.find("Project ID") != -1:
                        try:
                            soup = BeautifulSoup(driver.page_source, "lxml")
                            label_tag = soup.find("span", text="Project ID")
                            id_tag = label_tag.find_next_sibling("span")
                            data[int(id_tag.text)] = driver.current_url
                        except:
                            print("Failed to obtain Project ID for {0}".format(driver.current_url))
                            data[-1] = driver.current_url
                        driver.close()
                except:
                    print("Exception occurred checking if page ready. If you see this once, it's probably fine. If this keeps repeating, script has crashed.")

            # Avoid excessive CPU usage
            time.sleep(0.05)
                        
        print("Closing browser...")
        driver.quit()
        print("Done obtaining IDs.")
        return data

    def __make_driver(self, headless: bool) -> webdriver.Remote:
        if self.browser == Browser.Chrome:
            if headless:
                print("WARNING: ********************************************************************")
                print("WARNING: NOT USING HEADLESS MODE WITH CHROME AS IT PREVENTS FILE DOWNLOADS!!!")
                print("WARNING: ********************************************************************")
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif self.browser == Browser.Firefox:
            firefox_opts = webdriver.FirefoxOptions()
            firefox_opts.headless = headless
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_opts)
        else:
            raise Exception("Invalid browser")
