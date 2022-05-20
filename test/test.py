
from src.downloader import Browser, ModDownloader


if __name__ == "__main__":
    dl = ModDownloader(Browser.Chrome)
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/many-materials/")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/mob-opacity/")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/powah", "2915770")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/jei")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/journeymap")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/clumps")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/bookshelf")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/natures-compass")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/quark")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/patchouli")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/crafttweaker")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/enchantment-descriptions")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/storage-drawers")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/just-enough-resources-jer")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/ctm")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/iron-chests")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/tinkers-construct")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/curios")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/geckolib")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/chisel")
    dl.add_mod("https://www.curseforge.com/minecraft/mc-mods/architectury-api")
    dl.download()
