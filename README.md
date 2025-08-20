# Bhop CS2 Script

A modern, user-friendly application for controlling automated mouse scrolling, designed for bunny hopping in games. Built with PyQt6 for a sleek, responsive interface and optimized threading for minimal CPU usage.

## Features

- **Modern GUI**: Custom-designed translucent interface with orange/white theme
- **Configurable Controls**: Set custom activation key and scroll delay
- **Real-time Status**: Live status updates and visual feedback
- **Optimized Performance**: Event-driven threading for efficient CPU usage
- **Draggable Interface**: Move the window by dragging anywhere
- **Responsive Design**: Clean, intuitive controls with hover effects

## Requirements

- Python 3.7+
- PyQt6==6.9.1
- pynput
- keyboard

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Configure your settings:
   - **Activation Key**: Enter the key to hold for scrolling (default: space)
   - **Scroll Delay**: Set the delay between scroll events (default: 0.001 seconds)

3. Click **START** to begin
4. Hold the activation key to start scrolling
5. Release the key to stop scrolling
6. Click **STOP** to disable the script

## How It Works

- The application uses keyboard hooks to detect when you press/release the activation key
- When the key is held, it simulates continuous mouse wheel scrolling
- The scroller runs in a separate daemon thread for responsive performance
- All settings can be adjusted in real-time through the GUI

## Controls

- **START**: Activates the keyboard listener and enables scrolling
- **STOP**: Deactivates the keyboard listener and stops scrolling
- **Minimize (-)**: Minimize the application window
- **Close (X)**: Exit the application

## Technical Details

- **Threading**: Uses Python's threading module with event-driven architecture
- **Keyboard Handling**: Leverages the `keyboard` library for cross-platform key detection
- **Mouse Control**: Uses `pynput` for precise mouse scroll simulation
- **GUI Framework**: Built with PyQt6 for modern, responsive interface
- **Memory Management**: Proper cleanup of threads and keyboard hooks

## Safety Notice

This tool is designed for gaming purposes (bunny hopping). Please ensure compliance with the terms of service of any games you use it with.

## License

This project is open source. Feel free to modify and distribute.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

**Note**: This application requires appropriate permissions to control keyboard and mouse input. Make sure to run it with necessary privileges.
