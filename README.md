# 🎮 Bhop CS2 Script

# Description of improvements

Your app has been significantly improved with a focus on visual design, optimization, and functionality.

## ✨ New features

## Improved visual design
- **Modern interface** with gradients and animations
- **Semi-transparent background** with blur effect
- **Gradient buttons** with hover effects
- **Emoji icons** for better visualization
- **Rounded corners** and soft shadows

### 🔧 Optimized minimized mode
- **Compact mode** (320x120 px) for minimal space consumption
- **Fast switching** between full and compact mode
- **Animation of resizing** when switching modes
- **Status display** in compact mode
- **The control buttons** are available in both modes

## Improved binding system
- **Hold Mode** - Classic key hold mode
- **Toggle Mode** - toggle mode (pressed -on, pressed - off)
- **Extended list of keys**:
- Space, Ctrl, Alt, Shift
- Mouse4, Mouse5
- Any letter keys (F, V, C, etc.)
-**Combo box** with preset keys and the ability to enter your own

### 🎯 Advanced scrolling settings
- **Delay adjustment** from 1 to 1000 ms
- **Scroll force setting** from 1 to 10
- **Smooth scrolling** with interpolation
- **Scroll acceleration** when held for a long time
- **Visual indication** of current settings

### 💾 Configuration system
- **Auto-save settings** every 30 seconds
- **Loading settings** at startup
- **config.json file** for storing preferences
- **Saving the state** of all parameters

### 🔔 System Tray
- **Tray icon** for quick access
- **Context menu** with Show/Quit options
- **Double click** to open the window
- **Work in the background** while minimizing

### 🏗️ Architectural improvements
- **MVC pattern** for logic separation
- **Error handling** at all levels
- **Logging** of all actions
- **Thread safety** for the scroller
- **Event-driven architecture** for minimal CPU usage

## 📁 File structure

```
C:\bhop-cs2\
├── gui.py # GUI with animations
├── main.py # Main Module
├── scroller.py # Scroller
├── config.json # Settings file (created automatically)
README.md ``


## 🚀 Launch

```bash
python main.py
```

## 🎮 Usage

1. **Key Selection**: Select or enter the activation key
2. **Operating mode**: 
   - ✅ Hold Mode - hold to scroll
    Toggle Mode - press to turn on/off
3. **Parameter settings**:
- Delay: scrolling speed (less = faster)
- Strength: scrolling power (more = further)
4. **Press START** to activate
5. **Compact mode**: Press ◉ to switch

## 🔥 Keyboard shortcuts

- **Selected key** - scroll activation
- **◉ button** - switch compact mode
- **— button** - collapse to taskbar
- **✕ button** - close the application

## ⚙️ Requirements

- Python 3.8+
- PyQt6
- keyboard
- pynput

## 📝 Notes

- Some functions may need to be run by an administrator.
- The settings are automatically saved in `config.json`
- The app stays on top of all windows for easy access
- Compact mode is ideal for playing - it takes up a minimum of space

## 🎨 Color scheme

- **Main**: Orange (#FFA500)
- **Accent**: Dark Orange (#FF8C00)
- **Background**: White gradient with a slight tint
- **Status**: Green (active) / Orange (stopped)

## 🔧 Optimizations

1. **CPU usage**: Minimal due to the event-driven architecture
2. **Memory**: Optimized memory usage
3. **Responsiveness**: Instant response to user actions
4. **Stability**: Improved error handling prevents crashes

---
**Author**: Nerve11
**License**: MIT
