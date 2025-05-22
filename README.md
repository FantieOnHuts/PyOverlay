# Pythons stealth overlay.

This project is an experimental desktop overlay application built with Python and PyQt5. It creates a semi-transparent, always-on-top web browser window that can be made click-through and nearly invisible using global hotkeys.

The initial motivation for this project was to investigate the feasibility of using overlay windows to bypass or interact with restrictive software environments, such as exam proctoring software, inspired by the "LeetCode incident"

**Current Stage:** This is an early proof-of-concept and far from a polished or undetectable tool. It currently demonstrates basic overlay, transparency, and click-through functionality on Windows.

## ⚠️ Disclaimer

**This tool is intended for educational, research, and experimental purposes ONLY.**

*   **Do NOT use this tool for any unethical purposes, including cheating on exams or violating terms of service of any application or platform.** Engaging in such activities can have serious academic, professional, and legal consequences.
*   The author(s) of this project are not responsible for any misuse of this software.
*   Be aware that sophisticated proctoring software may have methods to detect overlays or unusual window behavior. This tool makes no guarantees of being undetectable.

## Features

*   **Always-on-Top Window:** The overlay window stays on top of other applications.
*   **Web Engine Integration:** Uses `QWebEngineView` (based on Chromium) to display web content (defaults to Google.com).
*   **Adjustable Opacity:** Default opacity is semi-transparent (85%).
*   **Toggle Visibility (Opacity):**
    *   Press `F9` to toggle the window between its default opacity and nearly invisible (1% opacity).
*   **Toggle Click-Through:**
    *   Press `F8` to toggle whether mouse clicks pass through the overlay window to the application underneath or interact with the overlay window.
*   **Kill switch:**
    *   Press `F10` twice to quit the app.

## How It Works (Technical Overview)

The application uses:
*   **PyQt5:** For the graphical user interface, window management, and embedding the web engine.
*   **QWebEngineView:** To render web pages within the Qt application.
*   **ctypes & Windows API:** To interact with the Windows operating system at a lower level:
    *   `SetWindowLongW` and `GetWindowLongW` are used to modify window styles.
    *   `WS_EX_LAYERED`: Allows the window to be transparent.
    *   `WS_EX_TRANSPARENT`: Makes the window click-through (mouse events pass through it).
    *   `WS_EX_TOOLWINDOW`: Prevents the window from appearing in the taskbar or Alt+Tab switcher (typical for tool windows).
*   **`keyboard` library:** To listen for global hotkeys (F8, F9) to control the overlay's behavior without needing the window to be focused.

## Requirements

*   Windows Operating System (due to Windows API calls for click-through)
*   Python 3.x
*   PyQt5
*   keyboard

## Installation

1.  **Clone the repository or download the Python script.**
    ```bash
    # If you're using Git
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Get the right python version**
    Version 3.13.3 workes for sure.

3. **To run**
    The included bat file has everything you need to start.
    It automaticaly installs the dependencies and creates the virual room.


## Current Limitations & Known Issues

*   **Windows-Only:** The click-through functionality relies on Windows-specific API calls.
*   **Detection:** This is a basic implementation. Advanced proctoring software might detect the presence of such an overlay, the Python interpreter, or the `keyboard` hook.
*   **Hardcoded URL:** The initial URL (Google.com) is hardcoded. You'll need to modify the source code (`self.browser.setUrl(QUrl("https://www.google.com"))`) to change it.
*   **Error Handling:** While some error handling is present (e.g., for `keyboard` import), it can be further improved.

## Future Ideas & Potential Enhancements

The user's vision for this project includes:
*   **Dynamic Content:** Easily load different web pages, potentially a ChatGPT interface.
*   **Stealthier Hiding:** Investigate methods to hide the application more effectively, perhaps by embedding it within a seemingly benign process or even exploring interactions at a driver level (e.g., "hide it in a mouse like a driver"). *This is a very advanced and significantly different challenge.*
*   **Toggle via Mouse Driver:** Control the overlay's visibility/interactivity through custom mouse driver events.
*   **Configuration:** Add a settings file or GUI to configure URL, opacity, hotkeys, etc.
*   **Cross-Platform Support:** Abstract OS-specific calls for wider compatibility (a major undertaking).
*   **Improved Stealth:** Research and implement techniques to reduce detectability.

## Contributing

This project is currently a personal experiment. If you have suggestions or want to contribute, feel free to open an issue or submit a pull request, maybe even fork.

---

*This README was partially AI generated based on the provided Python script and project description.*
