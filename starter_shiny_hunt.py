# This assumes you have a load state next to the starter you're going to select
# aaaaaaaadowna(can probs check 1st pokemon slot now)

import pyboy
from pyboy import PyBoy, WindowEvent
import time
from gameboy_memory_service import Gameboy_Memory_Service

# Define your list of inputs
input_sequence = "AAAAAAAAAAAAA"

# Initialize PyBoy with the ROM file and the save state file
pyboy = PyBoy('roms/crystal.gbc')
state = open("roms/crystal.gbc.state", "rb")
pyboy.load_state(state)
memory_service = Gameboy_Memory_Service(pyboy)

def shiny_hunt_loop(attempts=1): 
        
    # Counter for tracking frames
    frame_counter = 0

    # Loop through the input sequence
    for input_command in input_sequence:
        while frame_counter < 20:
            pyboy.tick()
            pyboy.tick()
            pyboy.tick()
            pyboy.tick()
            pyboy.tick()
            frame_counter += 1
        
        # Reset the frame counter
        frame_counter = 0

        # Press and hold the corresponding button
        if input_command == 'A':
            pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
        elif input_command == 'D':
            pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)

        # Release the button after 1 frame to simulate a button press and release
        pyboy.tick()
        pyboy.tick()
        pyboy.tick()
        if input_command == 'A':
            pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        elif input_command == 'D':
            pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)

    print ("DONE STARTER INPUT")
    is_shiny = memory_service.is_first_party_pokemon_shiny()
    info = memory_service.get_first_party_pokemon_info()
    print(f"Pokemon Species: {info[0]}, Level: {info[1]}, Gender: {info[2]}, Shiny: {'shiny' if is_shiny else 'not shiny'}")
    print("Number of resets: " + str(attempts))

    if not is_shiny:
        state = open("roms/crystal.gbc.state", "rb")
        pyboy.load_state(state)
        attempts = attempts + 1
        shiny_hunt_loop(attempts)

shiny_hunt_loop()

while not pyboy.tick():
    pass
pyboy.stop()







