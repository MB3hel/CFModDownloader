# CFModDownloader

## About

CurseForge mod downloader. This program can "automate" downloading of Minecraft mods from CurseForge using a web browser (chrome of firefox). This requires the url of the mod and the file id for the specific version. This information can be obtained either from navigating the CurseForge site or from a modpack manifest file. If using a modpack manifest file, you are provided with both the mod ID and file ID. The mod ID can be used to get the url using the CF API's "get mod" (requires you have a CF API Key&ast;). The intent of this project is to allow third party tools that have such an API key to download mods that may not allow third party downloads. Such a tool would need to create a list of mod urls and file versions from the modpack json (or from any other source) and pass it to this program when calling it. 

&ast;I think this part of the API still works for mods that disable third party usage, but I haven't actually confirmed this...

Instead of embedding a python program in such a tool (that is likely not written in python) there are other language bindings for the `selenium` library that can be used. If instead you would rather embed or download this python program (or pyinstaller binaries) that also works.


## Why?

I use Linux and Windows to play modded minecraft. I can't use the official CurseForge app on Linux and am not too inclined to install unnecessary bloatware (Overwolf platform) for it on Windows. I also like the features of various third party launchers. The new CF API has limited the use of those tools. This is one way to work around those limitations.


## License

MIT License (see LICENSE file for details)


## Demo usage

```sh
# Specify browser with -b
# Specify file to load modlist from with -f (can specify multiple)
# Specify mods on command line with -m
# Specify destination with -d
# Mods are specified in format of url:file_id
# Modpacks provide mod_id and file_id
# To get url from mod_id you need an api key and the url can be obtained by "getting the mod" using the CF API
python3 src/main.py -f modfile.txt -f modfile2.txt -m "https://www.curseforge.com/minecraft/mc-mods/waystones:3515707" -b firefox -d mods
```

Pyinstaller executables are also provided under releases and can be used instead of `python3 src/main.py`.


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
pyinstaller .\src\main.py --onefile --name cfmdown
```

**macOS:**

```sh
pyinstaller ./src/main.py --onefile --name cfmdown
```

**Linux:**

```sh
pyinstaller ./src/main.py --onefile --name cfmdown
```
