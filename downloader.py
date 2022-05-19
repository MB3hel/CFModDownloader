import shutil
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os
import argparse
from pathlib import Path
import time


if __name__ == "__main__":
    # Parse command line arguments for this script
    parser = argparse.ArgumentParser(description="Download CurseForge mods using a web browser.")
    parser.add_argument("url", type=str, help="URL to CurseForge page of mod to download.")
    parser.add_argument("dest", type=str, help="Folder to download mods into.")
    parser.add_argument("browser", type=str, choices=["chrome", "firefox"], help="Which browser to use to download mods.")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tempdir:
        dl_path = str(Path(tempdir).absolute()).replace("/", os.path.sep).replace("\\", os.path.sep)
        if dl_path[1] == ":":
            dl_path = dl_path[0].capitalize() + dl_path[1:]

        # Chrome options to download files to the specified directory without prompting the user
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_experimental_option("prefs", {
            "download.default_directory": dl_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })


        # Firefox options to download files to the specified directory without prompting the user
        firefox_opts = webdriver.FirefoxOptions()
        firefox_opts.set_preference("browser.download.folderList", 2)
        firefox_opts.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_opts.set_preference("browser.download.dir", dl_path)

        # Create driver for selected browser
        if args.browser == "chrome":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_opts)
        elif args.browser == "firefox":
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_opts)
        
        # Store original file count
        filecount_start = len(os.listdir(dl_path))

        # Start download
        driver.get("{0}/download".format(args.url))

        # Wait for download to start (either temp file or final file is written to dest directory)
        filecount_curr = filecount_start
        while filecount_curr == filecount_start:
            time.sleep(1)
            filecount_curr = len(os.listdir(dl_path))
        
        
        # Wait for download to finish (no temp file anymore)
        done = False
        while True:
            done = True
            for file in os.listdir(dl_path):
                if file.endswith(".crdownload"):
                    # Chrome in-progress downloads
                    done = False
                elif file.endswith(".part"):
                    # Firefox in-progress downloads
                    done = False
            if done:
                break
            time.sleep(1)

        # Download done. Make sure browser closes (some stay open once script exists, others don't)
        driver.close()
        
        # Create destination folder if needed
        dest_path = str(Path(args.dest).absolute())
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)

        # Copy downloaded files to destination folder (overwriting existing files)
        for file in os.listdir(tempdir):
            src = os.path.join(tempdir, file)
            dst = os.path.join(dest_path, file)
            if os.path.exists(dst):
                os.remove(dst)
            shutil.copy(src, dst)
    