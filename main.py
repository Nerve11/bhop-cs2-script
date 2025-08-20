import sys
import keyboard
from PyQt6.QtWidgets import QApplication
from gui import BhopAppGUI
from scroller import ScrollOnHold

class BhopApp:
    """
    Main application class.
    Connects the GUI to the scroller logic and manages the application state.
    """
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.gui = BhopAppGUI()
        self.scroller = ScrollOnHold()

        self.connect_signals()
        self.current_key = None
        self.press_hook = None
        self.release_hook = None

    def connect_signals(self):
        """Connects GUI button clicks to the corresponding functions."""
        self.gui.start_button.clicked.connect(self.start)
        self.gui.stop_button.clicked.connect(self.stop)

    def register_key_hooks(self):
        """Registers keyboard listeners for the activation key."""
        self.unregister_key_hooks() # Ensure no old hooks are present
        self.current_key = self.gui.key_input.text().strip().lower()
        try:
            self.press_hook = keyboard.on_press_key(self.current_key, lambda _: self.scroller.start_scrolling(), suppress=True)
            self.release_hook = keyboard.on_release_key(self.current_key, lambda _: self.scroller.stop_scrolling(), suppress=True)
        except Exception as e:
            print(f"Failed to register key '{self.current_key}': {e}")
            self.stop() # Stop the app if the key is invalid

    def unregister_key_hooks(self):
        """Removes all keyboard listeners."""
        if self.current_key:
            keyboard.unhook_all()
            self.current_key = None

    def start(self):
        """Starts the scroller thread and updates the GUI."""
        try:
            key = self.gui.key_input.text().strip().lower()
            delay = self.gui.delay_input.value()
            
            self.scroller.update_settings(key, delay)
            
            if not self.scroller.is_alive():
                self.scroller.start()
                
            self.register_key_hooks()
            self.gui.set_status_running()
            print(f"Scroller started. Press '{key}' to scroll.")
            
        except ValueError as e:
            print(f"Error starting scroller: {e}")
            # Optionally, show an error message in the GUI
            self.gui.status_label.setText(f"Error: {e}")
            self.gui.status_label.setStyleSheet("color: #FF0000;") # Red

    def stop(self):
        """Stops the scroller and keyboard listeners, and updates the GUI."""
        self.unregister_key_hooks()
        # The scroller thread itself keeps running in the background, 
        # waiting for activation. We just stop the *scrolling*.
        self.scroller.stop_scrolling() 
        self.gui.set_status_stopped()
        print("Scroller stopped.")

    def run(self):
        """Shows the GUI and starts the application event loop."""
        self.gui.show()
        # Ensure the scroller thread is terminated when the app closes
        self.app.aboutToQuit.connect(self.scroller.stop)
        sys.exit(self.app.exec())

if __name__ == '__main__':
    main_app = BhopApp()
    main_app.run()
