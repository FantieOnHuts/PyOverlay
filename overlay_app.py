import sys
import ctypes
from ctypes import wintypes

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings


GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000    
WS_EX_TRANSPARENT = 0x00000020  



user32 = ctypes.WinDLL('user32', use_last_error=True)

SetWindowLongW = user32.SetWindowLongW
SetWindowLongW.restype = wintypes.LONG 
SetWindowLongW.argtypes = [wintypes.HWND, wintypes.INT, wintypes.LONG]

GetWindowLongW = user32.GetWindowLongW
GetWindowLongW.restype = wintypes.LONG
GetWindowLongW.argtypes = [wintypes.HWND, wintypes.INT]

keyboard_available = False
try:
    import keyboard
    keyboard_available = True
    print("Keyboard module successfully imported.")
except ImportError:
    print("WARNING: The 'keyboard' module is not installed. Install it with 'pip install keyboard'.")
    print("Global hotkeys (F8, F9) will NOT work.")
except Exception as e:
    print(f"WARNING: Error importing/initializing 'keyboard' module: {e}")
    print("Global hotkeys (F8, F9) will NOT work.")
    print("This program may require administrator privileges for the 'keyboard' module to load/function correctly.")

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.is_effectively_visible = True
        self.is_click_through_enabled = False
        self.default_opacity_level = 0.85
        self.minimized_opacity_level = 0.01

        self.hwnd = None

        self.init_ui()
        self.setup_global_hotkeys()

    def init_ui(self):
        self.setWindowTitle("Transparent Overlay Window")
        self.setWindowFlags(
            Qt.FramelessWindowHint |        
            Qt.WindowStaysOnTopHint |       
            Qt.Tool                         
        )
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.setWindowOpacity(self.default_opacity_level)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.browser_view = QWebEngineView()
        web_profile = QWebEngineProfile.defaultProfile()
        web_profile.setHttpAcceptLanguage("en-US,en;q=0.9")


        web_settings = web_profile.settings()
        web_settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        web_settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        web_settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        web_settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        web_settings.setAttribute(QWebEngineSettings.DnsPrefetchEnabled, True)
        web_settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True) 

        self.browser_view.setUrl(QUrl("https://www.google.com"))
        self.main_layout.addWidget(self.browser_view)
        self.setLayout(self.main_layout)

        self.resize(800, 600)
        self.move(100, 100) 

    def setup_global_hotkeys(self):
        if not keyboard_available:
            print("Keyboard module not available, global hotkeys will not be registered.")
            return
        try:
            keyboard.add_hotkey('f9', self.toggle_effective_visibility, suppress=True)
            print("Hotkey F9 registered to toggle window visibility (opacity).")
            keyboard.add_hotkey('f8', self.toggle_click_through_mode, suppress=True)
            print("Hotkey F8 registered to toggle click-through mode.")
        except Exception as e:
            print(f"Error registering hotkeys (admin rights might be needed?): {e}")
            print("Ensure the script is run as administrator if hotkeys do not work.")

    def toggle_effective_visibility(self):
        print("F9 pressed: Toggling window visibility.")
        if self.is_effectively_visible:
            self.setWindowOpacity(self.minimized_opacity_level)
            self.is_effectively_visible = False
        else:
            self.setWindowOpacity(self.default_opacity_level)
            self.is_effectively_visible = True
        print(f"Window opacity set to: {self.windowOpacity():.2f}")

    def toggle_click_through_mode(self):
        if self.hwnd is None:
            print("Error: Window handle (HWND) not available. Cannot toggle click-through.")
            return

        print("F8 pressed: Toggling click-through mode.")
        current_ex_style = GetWindowLongW(self.hwnd, GWL_EXSTYLE)

        if not self.is_click_through_enabled:
            new_ex_style = current_ex_style | WS_EX_TRANSPARENT
            SetWindowLongW(self.hwnd, GWL_EXSTYLE, new_ex_style)
            self.is_click_through_enabled = True
            print("Click-through ENABLED (mouse events will pass through).")
        else:

            new_ex_style = current_ex_style & ~WS_EX_TRANSPARENT
            SetWindowLongW(self.hwnd, GWL_EXSTYLE, new_ex_style)
            self.is_click_through_enabled = False
            print("Click-through DISABLED (window is interactive).")
        
        self.update() 

    def showEvent(self, event):

        super().showEvent(event) 
        if self.hwnd is None:
            try:

                window_id_val = self.winId()
                if window_id_val:

                    self.hwnd = wintypes.HWND(int(window_id_val))
                    print(f"Window handle (HWND) obtained: {self.hwnd.value if self.hwnd else 'None'}")

                    current_ex_style = GetWindowLongW(self.hwnd, GWL_EXSTYLE)
                    if not (current_ex_style & WS_EX_LAYERED):
                        print("WS_EX_LAYERED not initially set by Qt. Setting it explicitly.")
                        SetWindowLongW(self.hwnd, GWL_EXSTYLE, current_ex_style | WS_EX_LAYERED)
                else:
                    print("Error: winId() returned an invalid value. Cannot obtain HWND.")
                    self.hwnd = None
            except Exception as e:
                print(f"Error obtaining/setting HWND in showEvent: {e}")
                self.hwnd = None 

    def closeEvent(self, event):
        print("Closing application...")
        if keyboard_available:
            try:
                keyboard.unhook_all_hotkeys()
                print("Global hotkeys unhooked.")
            except Exception as e:
                print(f"Error unhooking hotkeys during close: {e}")
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("StealthOverlayApp")
    app.setOrganizationName("Experimental")

    main_window = OverlayWindow()
    main_window.show()

    sys.exit(app.exec_())