
from downloader import Browser, ModDownloader

if __name__ == "__main__":
    dl = ModDownloader(Browser.Chrome)
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/many-materials/")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/mob-opacity/")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/powah")
    dl.download()