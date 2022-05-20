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
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os
import argparse
from typing import List
from pathlib import Path
import time
from enum import Enum, auto


class Browser(Enum):
    Chrome = auto()
    Firefox = auto()


class Mod:
    def __init__(self, base_url: str, file_id: str):
        self.base_url = base_url
        self.file_id = file_id    


## Downloader to download Minecraft Mods from CurseForge given the URL to the CurseForge page for the mod
#  Mods are downloaded using a browser on your system. Downloads are automated and require no user interaction.
class ModDownloader:

    ## Create downloader. All parameters are option and can be specified later.
    #  browser and dest have defaults. Mods must be added either in constructor or
    #  using add_mod function
    #  @param browser Specify which browser to download mods with
    #  @param dest Specify destination folder to download mods into
    #  @param mods Specify a set of urls for mods to download
    def __init__(self, browser: Browser = Browser.Chrome, dest = "./mods", mods = []):
        self.browser: Browser = browser
        self.dest: str = dest
        self.mods: List[Mod] = mods
        self.max_tabs = 0
    
    ## Add a mod to be downloaded using its url
    #  @param url CurseForge url to the mod to download
    def add_mod(self, url: str, file_id: str = ""):
        self.mods.append(Mod(url, file_id))

    ## Download the configured mods using the configured browser and destination folder
    #  This will open multiple browser windows, which will close automatically when done
    #  downloading. This function will not return until downloading is done
    def download(self):
        # Create temp dir to store downloaded files in
        print("Creating temp download directory...")
        with tempfile.TemporaryDirectory() as tempdir:
            # Construct properly formatted download path for use with browser options
            # Chrome on windows requires backslash and capitalized drive letter
            dl_path = str(Path(tempdir).absolute()).replace("/", os.path.sep).replace("\\", os.path.sep)
            if dl_path[1] == ":":
                dl_path = dl_path[0].capitalize() + dl_path[1:]

            # Create driver for selected browser
            print("Launching browser...")
            driver = self.__make_driver(dl_path)

            # For each set of mods (up to self.max_tabs mods per set)
            count = 1
            for mods in self.__split_mods_list():
                # Store original filecount (used to determine if all downloads have started)
                filecount_start = len(os.listdir(dl_path))
                
                # Start downloads (each in new tab)
                for mod in mods:
                    print("Starting download {0} of {1}...".format(count, len(self.mods)))
                    count = count + 1
                    if mod != mods[0]:
                        driver.switch_to.new_window('tab')
                    driver.execute_script("window.open('{0}/download/{1}', '_self');".format(mod.base_url, mod.file_id))
                
                # Wait for all downloads finish
                # Wait for filecount to increase by the same as the number of mods (excluding temp files)
                # and for there to be no temp files (temp = used by browser during download)
                # "While there are temp files or the filecount is too small"
                print("Waiting for all downloads to finish...")
                filecount_curr = filecount_start
                while filecount_curr < filecount_start + len(mods):
                    time.sleep(1)
                    lst = os.listdir(dl_path)
                    lst_notemp = []
                    for l in lst:
                        if l.endswith(".crdownload"):
                            # Chrome temp file
                            continue
                        if l.endswith(".part"):
                            # Firefox temp file
                            continue
                        lst_notemp.append(l)
                    filecount_curr = len(lst_notemp)

                # Even if enough non-temp files exist, the browser may still be copying to the new file
                # Do not continue until all temp files have been deleted by the browser
                print("Waiting for browser to finish...")
                done = False
                while not done:
                    time.sleep(1)
                    done = True
                    for file in os.listdir(dl_path):
                        if file.endswith(".crdownload"):
                            # Chrome temp file
                            done = False
                            break
                        if file.endswith(".part"):
                            # Firefox temp file
                            done = False
                            break
                
                # Close all but one tab so browser is ready for next set of mods
                for win in driver.window_handles[1:]:
                    driver.switch_to.window(win)
                    driver.close()
                
                # Switch to one remaining tab
                driver.switch_to.window(driver.window_handles[0])

            # Downloads all done. Close browser window now.
            print("Closing browser...")
            driver.quit()

            # Create destination folder if needed
            print("Preparing to copy to destination folder...")
            dest_path = str(Path(self.dest).absolute())
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            
            # Copy downloaded files to destination folder (overwriting existing)
            count = 1
            files = os.listdir(tempdir)
            for file in files:
                print("Copying file {0} of {1}".format(count, len(files)))
                count = count + 1
                src = os.path.join(tempdir, file)
                dst = os.path.join(dest_path, file)
                if os.path.exists(dst):
                    os.remove(dst)
                shutil.copy(src, dst)
        print("Done downloading mods.")
    
    ## Split self.mods into chunks of size self.max_tabs
    def __split_mods_list(self) -> List[List[Mod]]:
        # max_tabs == 0 means no limit
        if self.max_tabs == 0:
            return [self.mods.copy()]
        else:
            # Split into lists of size self.max_tabs
            result = []
            for i in range(0, len(self.mods), self.max_tabs):
                result.append(self.mods[i:i+self.max_tabs])
            return result

    def __make_driver(self, dl_path: str) -> webdriver.Remote:
        if self.browser == Browser.Chrome:
            # Chrome options to download files to the specified directory without prompting the user
            chrome_opts = webdriver.ChromeOptions()
            chrome_opts.add_experimental_option("prefs", {
                "download.default_directory": dl_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })
            chrome_opts.add_argument("--safebrowsing-disable-download-protection")
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_opts)
        elif self.browser == Browser.Firefox:
            # Firefox options to download files to the specified directory without prompting the user
            firefox_opts = webdriver.FirefoxOptions()
            firefox_opts.set_preference("browser.download.folderList", 2)
            firefox_opts.set_preference("browser.download.manager.showWhenStarting", False)
            firefox_opts.set_preference("browser.download.dir", dl_path)
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_opts)
        else:
            raise Exception("Invalid browser")
