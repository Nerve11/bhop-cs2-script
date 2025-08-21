import time
import threading
from pynput.mouse import Controller as MouseController
import keyboard

class AdvancedScroller(threading.Thread):
    """
    Advanced scrolling manager with multiple modes and precise controls.
    Features smooth scrolling, adjustable strength, and toggle/hold modes.
    """
    def __init__(self):
        super().__init__(daemon=True)
        self.mouse = MouseController()
        
        # Settings
        self.settings = {
            'key': 'space',
            'delay': 0.001,
            'strength': 1,
            'hold_mode': True,
            'smooth_scrolling': False,
            'acceleration': False
        }
        
        # State management
        self._scroll_active = threading.Event()
        self._shutdown = threading.Event()
        self._is_toggled = False
        self._scroll_counter = 0
        self._last_scroll_time = 0
        
        # Key hooks
        self._key_hooks = []
        
    def run(self):
        """
        Main scrolling thread with smooth scrolling support.
        """
        while not self._shutdown.is_set():
            self._scroll_active.wait()
            
            while self._scroll_active.is_set() and not self._shutdown.is_set():
                try:
                    # Calculate scroll strength with acceleration
                    strength = self.calculate_scroll_strength()
                    
                    # Perform scroll
                    if self.settings.get('smooth_scrolling', False):
                        self.smooth_scroll(strength)
                    else:
                        self.mouse.scroll(0, -strength)
                    
                    # Dynamic delay for smoother feel
                    delay = self.calculate_delay()
                    if delay > 0:
                        time.sleep(delay)
                        
                except Exception as e:
                    print(f"Error during scroll: {e}")
                    self._scroll_active.clear()
                    break
    
    def calculate_scroll_strength(self):
        """
        Calculates scroll strength with optional acceleration.
        """
        base_strength = self.settings.get('strength', 1)
        
        if self.settings.get('acceleration', False):
            # Accelerate scrolling over time
            current_time = time.time()
            if self._last_scroll_time > 0:
                elapsed = current_time - self._last_scroll_time
                if elapsed < 0.1:  # Within 100ms
                    self._scroll_counter += 1
                else:
                    self._scroll_counter = 0
            else:
                self._scroll_counter = 0
                
            self._last_scroll_time = current_time
            
            # Apply acceleration curve
            acceleration_factor = min(1 + (self._scroll_counter * 0.05), 3)
            return int(base_strength * acceleration_factor)
        
        return base_strength
    
    def calculate_delay(self):
        """
        Calculates dynamic delay based on settings.
        """
        base_delay = self.settings.get('delay', 0.001)
        
        if self.settings.get('smooth_scrolling', False):
            # Reduce delay for smoother scrolling
            return base_delay * 0.5
        
        return base_delay
    
    def smooth_scroll(self, strength):
        """
        Performs smooth scrolling with interpolation.
        """
        # Break large scrolls into smaller increments
        if strength > 1:
            for i in range(strength):
                self.mouse.scroll(0, -1)
                if i < strength - 1:
                    time.sleep(0.0001)  # Micro-delay for smoothness
        else:
            self.mouse.scroll(0, -strength)
    
    def start_scrolling(self):
        """Activates scrolling."""
        if not self._scroll_active.is_set():
            self._scroll_counter = 0
            self._last_scroll_time = 0
            self._scroll_active.set()
    
    def stop_scrolling(self):
        """Deactivates scrolling."""
        if self._scroll_active.is_set():
            self._scroll_active.clear()
            self._scroll_counter = 0
    
    def toggle_scrolling(self):
        """Toggles scrolling on/off."""
        if self._is_toggled:
            self.stop_scrolling()
            self._is_toggled = False
        else:
            self.start_scrolling()
            self._is_toggled = True
    
    def register_key_handlers(self):
        """Registers keyboard event handlers."""
        self.unregister_key_handlers()
        
        key = self.settings.get('key', 'space')
        hold_mode = self.settings.get('hold_mode', True)
        
        if hold_mode:
            # Hold-to-scroll mode
            on_press = keyboard.on_press_key(key, lambda _: self.start_scrolling(), suppress=True)
            on_release = keyboard.on_release_key(key, lambda _: self.stop_scrolling(), suppress=True)
            self._key_hooks = [on_press, on_release]
        else:
            # Toggle mode
            on_press = keyboard.on_press_key(key, lambda _: self.toggle_scrolling(), suppress=True)
            self._key_hooks = [on_press]
    
    def unregister_key_handlers(self):
        """Unregisters all keyboard event handlers."""
        for hook in self._key_hooks:
            try:
                keyboard.unhook(hook)
            except:
                pass
        self._key_hooks = []
    
    def update_settings(self, new_settings):
        """
        Updates scroller settings.
        
        Args:
            new_settings: Dictionary with settings like:
                - key: Activation key (string)
                - delay: Delay in milliseconds (int)
                - strength: Scroll strength 1-10 (int)
                - hold_mode: True for hold, False for toggle (bool)
                - smooth_scrolling: Enable smooth scrolling (bool)
                - acceleration: Enable scroll acceleration (bool)
        """
        # Convert delay from ms to seconds
        if 'delay' in new_settings:
            new_settings['delay'] = max(new_settings['delay'] / 1000.0, 0.0001)
        
        # Validate strength
        if 'strength' in new_settings:
            new_settings['strength'] = max(1, min(10, new_settings['strength']))
        
        # Update settings
        self.settings.update(new_settings)
        
        # Re-register key handlers if key or mode changed
        if 'key' in new_settings or 'hold_mode' in new_settings:
            if hasattr(self, '_key_hooks'):
                self.register_key_handlers()
    
    def stop(self):
        """Stops the scroller thread and cleans up."""
        self.unregister_key_handlers()
        self.stop_scrolling()
        self._shutdown.set()
        if self.is_alive():
            self.join(timeout=1.0)
    
    def get_status(self):
        """Returns current scroller status."""
        return {
            'active': self._scroll_active.is_set(),
            'toggled': self._is_toggled,
            'key': self.settings.get('key', 'space'),
            'mode': 'hold' if self.settings.get('hold_mode', True) else 'toggle',
            'strength': self.settings.get('strength', 1),
            'delay_ms': int(self.settings.get('delay', 0.001) * 1000)
        }


# For backwards compatibility
ScrollOnHold = AdvancedScroller
