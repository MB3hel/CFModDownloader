# CFModDownloader

## About `cfmdown`

CurseForge mod downloader. This program can "automate" downloading of Minecraft mods from CurseForge using a web browser (chrome of firefox). This requires the url of the mod and the file id for the specific version. This information can be obtained either from navigating the CurseForge site or from a modpack manifest file. If using a modpack manifest file, you are provided with both the mod ID and file ID. The mod ID can be used to get the url using the CF API's "get mod" (requires you have a CF API Key). The intent of this project is to allow third party tools that have such an API key to download mods that may not allow third party downloads. Such a tool would need to create a list of mod urls and file versions from the modpack json (or from any other source) and pass it to this program when calling it. 


**Demo usage:**

```sh
# Specify browser with -b
# Specify file to load modlist from with -f (can specify multiple)
# Specify mods on command line with -m
# Specify destination with -d
# Specify max parallel downloads with -t (0 for unlimited). Default is 12
# Mods are specified in format of url:file_id
# Modpacks provide mod_id and file_id
# To get url from mod_id you need an api key and the url can be obtained by "getting the mod" using the CF API
cfmdown -f modfile.txt -f modfile2.txt -m "https://www.curseforge.com/minecraft/mc-mods/waystones:3515707" -b firefox -d mods -t 0
```

Pyinstaller executables are also provided under releases and can be used instead of `python3 src/main.py`.


## About `cfmparse`

Curseforge Modpack Parser. This tool parses a CurseForge modpack zip file to determine base url and file id for all mods included *without using the CurseForge API*. Instead, a browser is used to navigate to each mod's page and search for its project id. This is a slower alternative to using the CF API to generate urls for mods. This program outputs a file that can be used by `cfmdown` to download the mods in a pack.

*Note: using firefox with this script instead of chrome is highly recommended as it seems to finish much faster*

**Demo Usage:**

```sh
# Use -b to select browser (chrome / firefox)
# Note: firefox is much faster for this script
# Use -t to specity number of browser tabs used
# Only positional argument is path to modpack zip downloaded from CF
# modfile_modpack.txt will be written next to modpack.zip
# If modpack name is <name>.zip output will be modfile_<name>.txt
cfmparse -b firefox -t 4 modpack.zip

# The resultant file can be used by cfmdown to download mods
cfmdown -b firefox -t 12 -d mods -f modfile_modpack.txt
```


## Why?

I use Linux and Windows to play modded minecraft. I can't use the official CurseForge app on Linux and am not too inclined to install unnecessary bloatware (Overwolf platform) for it on Windows. I also like the features of various third party launchers. The new CF API has limited the use of those tools. This is one way to work around those limitations.


## License

BSD 3 Clause (see LICENSE file for details)


## Dev Setup

```sh
python3 -m venv env

# Windows
.\env\scripts\activate
# Unix
source ./env/bin/activate

python -m pip install -r requirements.txt
```

The `test` folder contains development testing scripts.


## Building Executables

**Windows:**

```sh
pyinstaller .\src\cfmdown.py --onefile --name cfmdown
pyinstaller .\src\cfmparse.py --onefile --name cfmparse
```

**macOS:**

```sh
pyinstaller ./src/cfmdown.py --onefile --name cfmdown
pyinstaller ./src/cfmparse.py --onefile --name cfmparse
```

**Linux:**

```sh
pyinstaller ./src/cfmdown.py --onefile --name cfmdown
pyinstaller ./src/cfmparse.py --onefile --name cfmparse
```
