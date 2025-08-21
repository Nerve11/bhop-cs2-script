import sys
import os
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from gui import BhopAppGUI
from scroller_new import AdvancedScroller

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BhopController(QObject):
    """
    Main controller class managing the application logic.
    Implements MVC pattern for clean separation of concerns.
    """
    
    # Signals for status updates
    status_changed = pyqtSignal(str, str)  # message, color
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.scroller = None
        self.is_running = False
        self.current_settings = {}
        
    def initialize_scroller(self):
        """Initializes the scroller thread."""
        try:
            if self.scroller is None:
                self.scroller = AdvancedScroller()
                self.scroller.start()
                logger.info("Scroller thread initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize scroller: {e}")
            self.error_occurred.emit(f"Failed to initialize scroller: {e}")
            return False
    
    def start_scrolling(self, settings):
        """Starts the scrolling with given settings."""
        try:
            if not self.initialize_scroller():
                return False
            
            # Update scroller settings
            self.scroller.update_settings(settings)
            self.scroller.register_key_handlers()
            
            self.is_running = True
            self.current_settings = settings
            
            key = settings.get('key', 'space').upper()
            mode = "Hold" if settings.get('hold_mode', True) else "Toggle"
            
            self.status_changed.emit(
                f"✅ Active | Key: {key} | Mode: {mode}",
                "#00AA00"
            )
            
            logger.info(f"Scrolling started with key: {key}, mode: {mode}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start scrolling: {e}")
            self.error_occurred.emit(f"Failed to start: {str(e)}")
            return False
    
    def stop_scrolling(self):
        """Stops the scrolling."""
        try:
            if self.scroller:
                self.scroller.unregister_key_handlers()
                self.scroller.stop_scrolling()
                
            self.is_running = False
            self.status_changed.emit("⚫ Stopped", "#FF8C00")
            
            logger.info("Scrolling stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop scrolling: {e}")
            self.error_occurred.emit(f"Failed to stop: {str(e)}")
            return False
    
    def cleanup(self):
        """Cleanup resources on exit."""
        try:
            if self.scroller:
                self.scroller.stop()
                logger.info("Scroller thread stopped")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


class BhopApp:
    """
    Main application class connecting all components.
    """
    
    def __init__(self):
        # Initialize Qt application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Bhop Control")
        self.app.setOrganizationName("CS2 Tools")
        
        # Initialize components
        self.controller = BhopController()
        self.gui = BhopAppGUI()
        
        # Connect signals
        self.connect_signals()
        
        # Setup auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_settings)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
        
        logger.info("Application initialized")
    
    def connect_signals(self):
        """Connects all signals between components."""
        # GUI button connections
        self.gui.start_button.clicked.connect(self.on_start_clicked)
        self.gui.stop_button.clicked.connect(self.on_stop_clicked)
        
        # Compact mode buttons
        if hasattr(self.gui, 'compact_start'):
            self.gui.compact_start.clicked.connect(self.on_start_clicked)
            self.gui.compact_stop.clicked.connect(self.on_stop_clicked)
        
        # Controller status updates
        self.controller.status_changed.connect(self.update_status)
        self.controller.error_occurred.connect(self.show_error)
        
        # GUI settings changed
        self.gui.settings_changed.connect(self.on_settings_changed)
        
        # Application cleanup
        self.app.aboutToQuit.connect(self.cleanup)
    
    def on_start_clicked(self):
        """Handles start button click."""
        try:
            # Gather settings from GUI
            settings = {
                'key': self.gui.key_input.currentText() if hasattr(self.gui.key_input, 'currentText') else self.gui.key_input.text(),
                'delay': self.gui.delay_input.value(),
                'strength': self.gui.strength_slider.value() if hasattr(self.gui, 'strength_slider') else 1,
                'hold_mode': self.gui.hold_mode.isChecked() if hasattr(self.gui, 'hold_mode') else True
            }
            
            # Validate settings
            if not settings['key']:
                self.show_error("Please enter an activation key")
                return
            
            # Start scrolling
            if self.controller.start_scrolling(settings):
                self.set_ui_running(True)
                self.gui.save_settings()  # Save successful settings
                
        except Exception as e:
            logger.error(f"Error in start handler: {e}")
            self.show_error(f"Failed to start: {str(e)}")
    
    def on_stop_clicked(self):
        """Handles stop button click."""
        try:
            if self.controller.stop_scrolling():
                self.set_ui_running(False)
        except Exception as e:
            logger.error(f"Error in stop handler: {e}")
            self.show_error(f"Failed to stop: {str(e)}")
    
    def on_settings_changed(self, settings):
        """Handles settings changes from GUI."""
        try:
            if self.controller.is_running:
                # Update settings on the fly if running
                self.controller.scroller.update_settings(settings)
                logger.info("Settings updated on the fly")
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
    
    def update_status(self, message, color):
        """Updates status display in GUI."""
        try:
            self.gui.status_label.setText(message)
            self.gui.status_label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-size: 13pt;
                    font-weight: bold;
                    padding: 8px;
                    background-color: rgba(255, 165, 0, 10);
                    border-radius: 8px;
                }}
            """)
            
            # Update compact mode status
            if hasattr(self.gui, 'compact_status'):
                if "Active" in message:
                    self.gui.compact_status.setText("🟢")
                    self.gui.compact_status.setStyleSheet("QLabel { color: #00AA00; font-size: 20pt; }")
                else:
                    self.gui.compact_status.setText("⚫")
                    self.gui.compact_status.setStyleSheet("QLabel { color: #FF8C00; font-size: 20pt; }")
                    
        except Exception as e:
            logger.error(f"Error updating status: {e}")
    
    def show_error(self, message):
        """Shows error message to user."""
        logger.error(f"Error shown to user: {message}")
        
        # Update status label with error
        self.gui.status_label.setText(f"❌ Error: {message}")
        self.gui.status_label.setStyleSheet("""
            QLabel {
                color: #FF0000;
                font-size: 11pt;
                font-weight: bold;
                padding: 8px;
                background-color: rgba(255, 0, 0, 10);
                border-radius: 8px;
            }
        """)
        
        # Reset status after 3 seconds
        QTimer.singleShot(3000, lambda: self.update_status("⚫ Stopped", "#FF8C00"))
    
    def set_ui_running(self, running):
        """Updates UI state based on running status."""
        try:
            if running:
                # Normal view
                self.gui.start_button.setEnabled(False)
                self.gui.stop_button.setEnabled(True)
                self.gui.key_input.setEnabled(False)
                self.gui.delay_input.setEnabled(False)
                
                if hasattr(self.gui, 'strength_slider'):
                    self.gui.strength_slider.setEnabled(False)
                if hasattr(self.gui, 'hold_mode'):
                    self.gui.hold_mode.setEnabled(False)
                
                # Compact view
                if hasattr(self.gui, 'compact_start'):
                    self.gui.compact_start.setEnabled(False)
                    self.gui.compact_stop.setEnabled(True)
            else:
                # Normal view
                self.gui.start_button.setEnabled(True)
                self.gui.stop_button.setEnabled(False)
                self.gui.key_input.setEnabled(True)
                self.gui.delay_input.setEnabled(True)
                
                if hasattr(self.gui, 'strength_slider'):
                    self.gui.strength_slider.setEnabled(True)
                if hasattr(self.gui, 'hold_mode'):
                    self.gui.hold_mode.setEnabled(True)
                
                # Compact view
                if hasattr(self.gui, 'compact_start'):
                    self.gui.compact_start.setEnabled(True)
                    self.gui.compact_stop.setEnabled(False)
                    
        except Exception as e:
            logger.error(f"Error updating UI state: {e}")
    
    def auto_save_settings(self):
        """Auto-saves settings periodically."""
        try:
            if hasattr(self.gui, 'save_settings'):
                self.gui.save_settings()
                logger.debug("Settings auto-saved")
        except Exception as e:
            logger.error(f"Error auto-saving settings: {e}")
    
    def cleanup(self):
        """Cleanup on application exit."""
        try:
            logger.info("Application shutting down...")
            
            # Save settings
            self.auto_save_settings()
            
            # Stop auto-save timer
            self.auto_save_timer.stop()
            
            # Cleanup controller
            self.controller.cleanup()
            
            logger.info("Application shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def run(self):
        """Runs the application."""
        try:
            # Show GUI
            self.gui.show()
            
            # Start Qt event loop
            sys.exit(self.app.exec())
            
        except Exception as e:
            logger.critical(f"Critical error in main loop: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    try:
        # Check for admin rights on Windows
        if sys.platform == 'win32':
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                logger.warning("Running without administrator privileges. Some features may not work.")
        
        # Create and run application
        app = BhopApp()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
