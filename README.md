
# 🚀 Advanced Notepad 📝

## 🌟 Project Overview
**Advanced Notepad** is a *feature-packed*, cross-platform text editor crafted with **Python 3** and **PyQt6** 🐍💻. It delivers a sleek, tabbed interface with robust rich text editing, seamless drag-and-drop, and forward-looking features like interactive image resizing, theme switching, and placeholders for AI-driven tools (text-to-speech, speech-to-text) 🎙️📢. Perfect for developers, writers, and power users, this app blends performance, customization, and a delightful UX! 😎

## ✨ Key Features
- **Tabbed Document Interface** 📑: Juggle multiple documents with closable tabs and a handy `+` button for new ones.
- **Rich Text Editing** 🎨:
  - Format text with colors, fonts, and hyperlinks using HTML.
  - Tweak alignment and styles via intuitive dialogs.
- **Drag-and-Drop Magic** 🖱️:
  - Drop text files (`.txt`) or images (`.png`, `.jpg`, `.jpeg`, `.gif`) effortlessly.
  - Images embed with centered `<img>` tags.
- **Interactive Image Resizing** 🖼️:
  - Resize images by dragging corners with visual handles.
  - Right-click images for a "Resize Image" option.
- **Theme Switching** 🌗:
  - Flip between *dark* and *light* themes with dynamic styles.
  - Consistent across all tabs and editors.
- **File Operations** 💾:
  - Open, save, or save-as with UTF-8 encoding.
  - Handles all file types, optimized for text.
- **Edit Toolkit** ✂️:
  - Cut, copy, paste, find, replace, and select all with standard shortcuts (`Ctrl+S`, `Ctrl+F`).
- **Next-Gen Features** 🚀:
  - Insert hyperlinks for selected text 📎.
  - Pick text colors with a slick color dialog 🎨.
  - AI-ready: Text-to-speech and speech-to-text placeholders.
- **Extensible Design** 🛠️:
  - Modular classes (`Notepad`, `MyTextEdit`, `ResizableImageLabel`).
  - Ready for plugins or custom features.

## 🛠️ Technical Requirements
- **Python**: 3.8+ 🐍
- **PyQt6**: Install via `pip install PyQt6` 📦
- **OS**: Windows, macOS, Linux (PyQt6 is cross-platform) 🌍
- **Optional (Future)**:
  - `pyttsx3` for text-to-speech 📢
  - `speech_recognition` for speech-to-text 🎙️
  - `pydub` for audio processing 🔊

## 📦 Installation
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/saikumar-chev/advanced-notepad.git
   cd advanced-notepad
   ```
2. **Set Up Virtual Env** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install PyQt6
   ```
4. **Launch the App**:
   ```bash
   python notepad.py
   ```

## 🎮 Usage Guide
1. **Start the App** 🚀:
   - Run `python notepad.py` to open with an "Untitled" tab.
2. **File Management** 📂:
   - *New Tab*: `File > New` or `Ctrl+N`.
   - *Open*: `File > Open` or `Ctrl+O`.
   - *Save/Save As*: `Ctrl+S` or `Ctrl+Shift+S`.
3. **Editing** ✍️:
   - Use `Edit` menu for cut (`Ctrl+X`), copy (`Ctrl+C`), paste (`Ctrl+V`), find (`Ctrl+F`), replace (`Ctrl+R`), or select all (`Ctrl+A`).
   - Change fonts (`Font > Font`) or text color (`Features > Change Text Color`).
4. **Image Handling** 🖼️:
   - Drag and drop images to embed them.
   - Right-click and select "Resize Image" to adjust sizes interactively.
5. **Hyperlinks** 🔗:
   - Select text, then `Features > Insert Hyperlink` to add clickable links.
6. **Themes** 🌈:
   - Toggle dark/light modes via `Features > Toggle Dark/Light Theme`.
7. **AI Features** 🤖:
   - Text-to-speech and speech-to-text are placeholders; extend them with libraries.

## 🧩 Code Architecture
The codebase is split into three core classes in `notepad.py`:

- **ResizableImageLabel** (`QLabel` subclass) 🖼️:
  - Powers interactive image resizing with mouse-driven corner handles.
  - Key Methods: `mousePressEvent`, `mouseMoveEvent`, `paintEvent`.
- **MyTextEdit** (`QTextEdit` subclass) 📝:
  - Enhances QTextEdit with drag-and-drop and custom image context menus.
  - Key Methods: `dragEnterEvent`, `dropEvent`, `context_menu`.
- **Notepad** (`QMainWindow` subclass) 🖥️:
  - Orchestrates the tabbed UI, menus, and core functionality.
  - Key Methods: `new_tab`, `toggle_theme`, `insert_hyperlink`.

## 💡 Design Principles
- **Modular**: Clean, self-contained classes for easy maintenance.
- **Event-Driven**: Leverages PyQt6 signals/slots for responsiveness.
- **Cross-Platform**: Consistent UX across OSes via PyQt6.
- **User-First**: Intuitive shortcuts, visual cues, and drag-and-drop.

## ⚠️ Known Limitations
- **AI Features**: Text-to-speech and speech-to-text are stubs; need external libraries.
- **Image Resizing**: Corner-based only; no cropping or aspect ratio locks.
- **Rich Text**: Basic HTML support; lacks tables, lists, or advanced formatting.
- **Performance**: Large images/documents may lag due to HTML rendering.
- **Error Handling**: Limited validation for file ops or inputs.

## 🌟 Planned Enhancements
- **AI Integration** 🤖:
  - Add `pyttsx3` for text-to-speech.
  - Implement `speech_recognition` for speech-to-text.
- **Rich Text** 📜:
  - Support lists, tables, and inline styles.
  - Add a formatting toolbar.
- **Image Features** 🖼️:
  - Enable cropping, rotation, and aspect ratio preservation.
  - Support `.webp` and other formats.
- **File Handling** 💾:
  - Autosave and session recovery.
  - Recent files menu.
- **Performance** ⚡:
  - Optimize rendering for large files.
  - Thread heavy operations.
- **Accessibility** ♿:
  - Keyboard support for image resizing.
  - Screen reader compatibility.

## 🛠️ Development Setup
1. **Linting/Formatting**:
   - Install: `pip install flake8 black`.
   - Run: `flake8 notepad.py` and `black notepad.py`.
2. **Testing**:
   - Manual testing for now; future `pytest-qt` integration planned.
3. **Debugging**:
   - Use `pdb` or IDEs like PyCharm.
   - Log mouse events in `ResizableImageLabel` for resize debugging.

## 🤝 Contributing
Love to have you aboard! 🌟 To contribute:
1. Fork and create a branch:
   ```bash
   git checkout -b feature/<your-feature>
   ```
2. Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) and document code.
3. Test thoroughly.
4. Submit a PR with a clear description.

See our [Code of Conduct](CODE_OF_CONDUCT.md) and add tests for new features.

## 📜 License
Licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

## 🐛 Troubleshooting
- **PyQt6 Issues**:
  - Verify: `pip install PyQt6`.
  - Check Python version (3.8+).
- **Drag-and-Drop Fails**:
  - Ensure file paths/permissions are valid.
  - Confirm supported formats.
- **Theme Problems**:
  - Check `apply_theme` stylesheet syntax.
  - Look for Qt style conflicts.
- **Image Resizing Bugs**:
  - Validate image paths in `resize_image`.
  - Debug mouse events in `ResizableImageLabel`.

File issues on [GitHub](https://github.com/saikumar-chev/advanced-notepad) with repro steps.

## 🙌 Acknowledgments
- Powered by [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) 🚀
- Inspired by Notepad++, VS Code, and modern editors ✨

## 📬 Contact
Questions? Ideas? 🗣️
- Open an issue on [GitHub](https://github.com/saikumar-chev/advanced-notepad).
- Email: <chevellasaikumar31@gmail.com>.
