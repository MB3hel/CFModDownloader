# CFModDownloader

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

Pyinstaller executables are also provided under releases.


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
