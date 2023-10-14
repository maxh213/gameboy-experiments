from pyboy import PyBoy
pyboy = PyBoy('roms/crystal.gbc')
while not pyboy.tick():
    pass
pyboy.stop()