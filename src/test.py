
from downloader import ModDownloader

if __name__ == "__main__":
    dl = ModDownloader()
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/many-materials/")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/mob-opacity/")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/powah")
    dl.download()