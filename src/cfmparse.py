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
import tempfile
import traceback
from typing import Dict, List
import zipfile
import json
import os
from bs4 import BeautifulSoup
from mpparser import ModParser, Browser


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uses a browser to create a list of mod URLs for a CurseForge modpack zip.")
    parser.add_argument("-b", dest="browser", type=str, default="chrome", choices=["chrome", "firefox"], help="Specify which browser to use to download mods")
    parser.add_argument("-t", metavar="tabs", dest="tabs", type=int, default=4, help="Number of browser tabs to use for project id resolution. Number of concurrent resolutions.")
    parser.add_argument("modpack", type=str, help="Path to downloaded modpack zip file.")
    args = parser.parse_args()

    browser = None
    if args.browser == "chrome":
        browser = Browser.Chrome
    elif args.browser == "firefox":
        browser = Browser.Firefox

    # modid list
    modid_lst: List[int] = []

    # modid, fileid
    fileid_map: Dict[int, int] = {}

    # url list
    url_lst: List[str] = []

    # modid, modurl
    url_map: Dict[int, str] = {}

    with tempfile.TemporaryDirectory() as tempdir:
        # Extract relevant files to temporary directory
        print("Extracting files from modpack zip...")
        try:
            with zipfile.ZipFile(args.modpack) as zf:
                zf.extract('manifest.json', tempdir)
                zf.extract('modlist.html', tempdir)
        except:
            traceback.print_exc()
            print("Extracting modpack zip failed!")
            exit(1)

        # Read manifest to construct list of modIDs and map them to their fileIds
        print("Reading modpack manifest...")
        try:
            with open(os.path.join(tempdir, "manifest.json"), "r") as manifest_file:
                filedata = json.load(manifest_file)
            for file in filedata["files"]:
                modid = file["projectID"]
                fileid = file["fileID"]
                modid_lst.append(modid)
                fileid_map[modid] = fileid
        except:
            traceback.print_exc()
            print("Parsing manifest failed!")
            exit(1)
        
        # Read modlist html to construct list of urls
        print("Reading modlist...")
        try:
            with open(os.path.join(tempdir, "modlist.html"), "rb") as modlist_file:
                soup = BeautifulSoup(modlist_file.read().decode('utf-8'), "lxml")
                for a in soup.find_all('a'):
                    url_lst.append(a.get("href"))
        except:
            traceback.print_exc()
            print("Parsing modlist failed!")
            exit(1)
    
    # Done with extracted temporary files
    
    # Visit each url in a browser and get the project ID (= modID) associated with the URL
    print("Parsing mod pages to find mod IDs...")
    try:
        p = ModParser(url_lst, browser)
    except:
        print("Failed to parse one or more mod pages!")
        exit(1)
    p.num_tabs = args.tabs
    url_map = p.parse()
    if -1 in url_map.keys():
        print("Failed to parse one or more mod pages!")
        exit(1)

    
    print("Parsing pages done. Generating modfile...")
    mf_name = "modfile_{0}.txt".format(os.path.basename(args.modpack)[:-4])
    mf_path = os.path.join(os.path.dirname(args.modpack), mf_name)
    with open(mf_path, "w") as f:
        for modid in modid_lst:
            fileid = fileid_map[modid]
            url = url_map[modid]
            f.write("{0}:{1}\n".format(url, fileid))
    print("Modfile written to {0}".format(mf_path.replace("/", os.path.sep).replace("\\", os.path.sep)))