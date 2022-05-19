
import shutil
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
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
        self.mods: List[str] = []
        self.__drivers: List[webdriver.Remote] = []
    
    ## Add a mod to be downloaded using its url
    #  @param url CurseForge url to the mod to download
    def add_mod(self, url: str):
        if not url in self.mods:
            self.mods.append(url)
    
    ## Download the configured mods using the configured browser and destination folder
    #  This will open multiple browser windows, which will close automatically when done
    #  downloading. This function will not return until downloading is done
    def download(self):
        # Clear old state
        self.__drivers.clear()

        # Create temp dir to store downloaded files in
        with tempfile.TemporaryDirectory() as tempdir:
            # Construct properly formatted download path for use with browser options
            # Chrome on windows requires backslash and capitalized drive letter
            dl_path = str(Path(tempdir).absolute()).replace("/", os.path.sep).replace("\\", os.path.sep)
            if dl_path[1] == ":":
                dl_path = dl_path[0].capitalize() + dl_path[1:]

            # Store original filecount (used to determine if all downloads have started)
            filecount_start = len(os.listdir(dl_path))

            # Start downloads
            for mod in self.mods:
                self.__download(mod, dl_path)
            
            # Wait for all downloads to of finish
            # Wait for filecount to increase by the same as the number of mods
            # and for there to be no temp files (temp = used by browser during download)
            # "While there are temp files or the filecount is too small"
            filecount_curr = filecount_start
            aretemp = True
            while aretemp or (filecount_curr < filecount_start + len(self.mods)):
                time.sleep(1)
                lst = os.listdir(dl_path)
                aretemp = False
                for l in lst:
                    if l.endswith(".crwodnwload"):
                        # Chrome
                        aretemp = True
                    if l.endswith(".part"):
                        # Firefox
                        aretemp = True
                filecount_curr = len(lst)
            
            # Download done. Close browser windows now.
            for driver in self.__drivers:
                driver.close()
            
            # Create destination folder if needed
            dest_path = str(Path(self.dest).absolute())
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            
            # Copy downloaded files to destination folder (overwriting existing)
            for file in os.listdir(tempdir):
                src = os.path.join(tempdir, file)
                dst = os.path.join(dest_path, file)
                if os.path.exists(dst):
                    os.remove(dst)
                shutil.copy(src, dst)
            

    def __download(self, url: str, dl_path: str) -> webdriver.Remote:
        if self.browser == Browser.Chrome:
            # Chrome options to download files to the specified directory without prompting the user
            chrome_opts = webdriver.ChromeOptions()
            chrome_opts.add_experimental_option("prefs", {
                "download.default_directory": dl_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_opts)
        elif self.browser == Browser.Firefox:
            # Firefox options to download files to the specified directory without prompting the user
            firefox_opts = webdriver.FirefoxOptions()
            firefox_opts.set_preference("browser.download.folderList", 2)
            firefox_opts.set_preference("browser.download.manager.showWhenStarting", False)
            firefox_opts.set_preference("browser.download.dir", dl_path)
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_opts)
        else:
            raise Exception("Invalid browser")
        driver.get("{0}/download".format(url))
        self.__drivers.append(driver)
