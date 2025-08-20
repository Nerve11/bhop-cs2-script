import time
import threading
from pynput.mouse import Controller as MouseController
import keyboard

class ScrollOnHold(threading.Thread):
    """
    Manages the mouse scrolling in a separate thread.
    Optimized for low CPU usage with an event-driven model.
    """
    def __init__(self):
        super().__init__(daemon=True)
        self.mouse = MouseController()
        self.activate_key = 'space'
        self.scroll_delay = 0.001
        
        self._scroll_active = threading.Event()
        self._shutdown = threading.Event()
        self._running = False

    def run(self):
        """
        The main loop for the scrolling thread.
        Waits for events to avoid unnecessary CPU cycles.
        """
        self._running = True
        while not self._shutdown.is_set():
            # Wait efficiently until scrolling is activated
            # Wait efficiently until scrolling is activated
            self._scroll_active.wait()

            # Once active, scroll until told to stop
            while self._scroll_active.is_set() and not self._shutdown.is_set():
                try:
                    self.mouse.scroll(0, -1)
                    time.sleep(self.scroll_delay)
                except Exception as e:
                    print(f"Error during scroll: {e}")
                    # Stop scrolling on error to prevent loops
                    self._scroll_active.clear()
                    break
        self._running = False

    def start_scrolling(self):
        """Activates the scroll loop."""
        if self._running and not self._scroll_active.is_set():
            self._scroll_active.set()

    def stop_scrolling(self):
        """Deactivates the scroll loop."""
        if self._scroll_active.is_set():
            self._scroll_active.clear()

    def stop(self):
        """Signals the thread to shut down gracefully."""
        self._scroll_active.clear()
        self._shutdown.set()
        if self.is_alive():
            self.join(timeout=1.0)

    def update_settings(self, activate_key, scroll_delay):
        """Updates the activation key and scroll delay."""
        if not isinstance(scroll_delay, (int, float)) or scroll_delay <= 0:
            raise ValueError("Scroll delay must be a positive number")
        if not isinstance(activate_key, str) or not activate_key:
            raise ValueError("Activation key must be a non-empty string")
            
        self.activate_key = activate_key
        self.scroll_delay = scroll_delay
