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
