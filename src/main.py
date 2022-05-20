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


import argparse
import os
import traceback
import shutil
from typing import Tuple
from downloader import ModDownloader, Browser



def parse_mod(mod: str) -> Tuple[str, str]:
    if mod.count(":") != 2:
        print("Invalid mod format: '{0}'".format(mod))
        exit(1)
    colon_pos = mod.rfind(":")
    url = mod[0:colon_pos]
    file_id = mod[colon_pos+1:]
    return url, file_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uses a browser to download Minecraft mods from CurseForge")
    parser.add_argument("-b", dest="browser", type=str, default="chrome", choices=["chrome", "firefox"], help="Specify which browser to use to download mods")
    parser.add_argument("-d", dest="dest", default="./mods", type=str, metavar="destination", help="Destination folder to download mods to. Will be created it it does not exist.")
    parser.add_argument("-m", dest="mods", metavar="mod", default=[], action="append", type=str, help="Download a given mod in the form url:file_id")
    parser.add_argument("-f", dest="files", metavar="file", default=[], action="append", type=str, help="Download mods listed in the given file in the form url:file_id")
    parser.add_argument("-t", dest="tabs", metavar="tabs", default=0, type=int, help="Maximum number of tabs (concurrent mod downloads) at a time. 0 for unlimited. Default 0")
    args = parser.parse_args()
    if len(args.mods) == 0 and len(args.files) == 0:
        parser.error("No mods provided. Use either -m or -f when invoking.")

    browser = None
    if args.browser == "chrome":
        browser = Browser.Chrome
    elif args.browser == "firefox":
        browser = Browser.Firefox

    dl = ModDownloader(browser, args.dest)
    dl.max_tabs = args.tabs

    for mod in args.mods:
        url, file_id = parse_mod(mod)
        dl.add_mod(url, file_id)
    
    for file in args.files:
        if not os.path.exists(file):
            print("Error: File {0} not found!".format(file))
            exit(1)
        try:
            with open(file, "r") as f:
                for line in f.readlines():
                    if line.startswith("#"):
                        continue
                    url, file_id = parse_mod(line.replace("\n", "").replace("\r", ""))
                    dl.add_mod(url, file_id)
        except:
            print("Error: Error opening or reading {0}".format(file))
            exit(1)
    
    try:
        dl.download()
        print("Downloaded mods successfully!")
    except:
        traceback.print_exc()
        print("Downloading mods failed!")
        exit(1)
