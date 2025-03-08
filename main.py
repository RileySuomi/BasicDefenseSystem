from pynput import keyboard, mouse

class afkScript:
    def __init__(self, activation_key=keyboard.Key.shift_r):

        self.activation_key = activation_key
        self.defense_monitor = False

        # need a track of mouse positioning
        self.last_position = None

        # listeners
        self.keyboard_listener = None
        self.mouse_listener = None

    def start(self):

        print("Defense System is running...")

        # start program that runs the listeners
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_move=self.on_move)
        self.keyboard_listener.start()
        self.mouse_listener.start()

        self.keyboard_listener.join()
        self.mouse_listener.join()

    def stop(self):

        # stop the listeners
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def on_press(self, key):

        # check if the activation key is pressed 
        if key == self.activation_key:
            self.defense_monitor = not self.defense_monitor
            print("Defense mode is: ACTIVATE")
          
        #deactivation key pressed
        elif key == keyboard.Key.esc:
            self.defense_monitor = False
            self.stop()
            print("Defense system has been: DEACTIVATED")

    def on_move(self, x, y):

      # if in defense mode, on_move tracks if the mouse is being moved and sends alerts until defense mode turned off
      
        current_position = (x, y)

        if self.defense_monitor:
            if self.last_position is None: # need to update
                self.last_position = current_position
                print("You are no longer AFK:")
                print(current_position)
            else:
                print("MOVEMENT DETECTED")
                #print(f"from {self.last_position} to {current_position}")
                self.last_position = current_position
                
        else:
            self.last_position = current_position


if __name__ == "__main__":
    security = afkScript(activation_key=keyboard.Key.shift_r)
    try:
        security.start()
    except KeyboardInterrupt:   
        security.stop()
