import pyboy
from pyboy import PyBoy, WindowEvent
import threading
from gameboy_memory_service import Gameboy_Memory_Service
import sys
import random
import time

# Define your list of inputs
input_sequence = "AAAAAAAAAAAAA"

# Shared variable and lock for tracking total attempts
total_attempts = 0
attempts_lock = threading.Lock()

# Shared variable and lock for tracking whether a shiny has been found
shiny_found = False
shiny_found_lock = threading.Lock()

def shiny_hunt_loop(pyboy, memory_service):
    global total_attempts  # Access the global total_attempts variable
    global shiny_found  # Access the global shiny_found variable
    while True:  # Change loop condition to True
        with shiny_found_lock:  # Acquire the lock to read shiny_found
            if shiny_found:  # Check shiny_found within the lock
                print ("Closing down all threads - shiny found!!!")
                break  # Exit the loop if shiny_found is True
        
        # Counter for tracking frames
        frame_counter = 0

        """
        Waits for a random number of emulator ticks between min_ticks and max_ticks.
        
        Args:
        - min_ticks (int): The minimum number of ticks to wait.
        - max_ticks (int): The maximum number of ticks to wait.
        """
        min_ticks = 0
        max_ticks = 9000
        random.seed(time.time())  # Seed the random number generator with the current time
        num_ticks = random.randint(min_ticks, max_ticks)
        for _ in range(num_ticks):
            pyboy.tick()

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

        is_shiny = memory_service.is_first_party_pokemon_shiny()        

        if not is_shiny:
            with attempts_lock:  # Acquire the lock to update total_attempts
                total_attempts += 1
                current_attempts = total_attempts  # Store the current total for printing
                memory_service.print_first_party_pokemon_info(current_attempts)
            state = open(f"roms/crystal.gbc.state", "rb")
            pyboy.load_state(state)
        else:
            memory_service.print_first_party_pokemon_info(current_attempts)
            state = open("roms/crystal.gbc.state", "wb")
            pyboy.save_state(state)
            with shiny_found_lock:  # Acquire the lock to update shiny_found
                shiny_found = True  # Set shiny_found to True when a shiny is found

def run_emulator():
    # Initialize PyBoy with the ROM file and the save state file
    pyboy = PyBoy(f'roms/crystal.gbc', window_type='headless', hide_window='--quiet' in sys.argv)
    state = open(f"roms/crystal.gbc.state", "rb")
    pyboy.load_state(state)
    memory_service = Gameboy_Memory_Service(pyboy)

    # Start the shiny hunt loop
    shiny_hunt_loop(pyboy, memory_service)

    pyboy.stop()

def run_emulator_window():
    # Initialize PyBoy with the ROM file and the save state file
    pyboy = PyBoy(f'roms/crystal.gbc')
    state = open(f"roms/crystal.gbc.state", "rb")
    pyboy.load_state(state)
    memory_service = Gameboy_Memory_Service(pyboy)

    # Start the shiny hunt loop
    shiny_hunt_loop(pyboy, memory_service)

    pyboy.stop()



if __name__ == "__main__":  
    run_emulator()
    # run_emulator_window()

    # # Create and start threads for each emulator instance
    # emulator_threads = [threading.Thread(target=run_emulator) for _ in range(500)]
    # for thread in emulator_threads:
    #     thread.start()

    # # Wait for all threads to complete
    # for thread in emulator_threads:
    #     thread.join()

