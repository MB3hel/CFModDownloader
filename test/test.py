#
# MIT License
# 
# Copyright (c) 2022 Marcus Behel
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 


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
