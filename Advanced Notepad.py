import sys
import os
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class ResizableImageLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        self.setFixedSize(500, 500)
        self.original_pixmap = pixmap
        self.is_resizing = False
        self.resize_handle_size = 10
        self.current_handle = None

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.current_handle:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.PenStyle.SolidLine))
            painter.setBrush(QBrush(Qt.GlobalColor.black))
            for x, y in self.current_handle:
                painter.drawRect(QRect(x, y, self.resize_handle_size, self.resize_handle_size))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.current_handle = []
            if self._is_near_corner(pos, 0, 0):
                self.current_handle.append((0, 0))
            elif self._is_near_corner(pos, self.width() - self.resize_handle_size, 0):
                self.current_handle.append((self.width() - self.resize_handle_size, 0))
            elif self._is_near_corner(pos, 0, self.height() - self.resize_handle_size):
                self.current_handle.append((0, self.height() - self.resize_handle_size))
            elif self._is_near_corner(pos, self.width() - self.resize_handle_size,
                                      self.height() - self.resize_handle_size):
                self.current_handle.append(
                    (self.width() - self.resize_handle_size, self.height() - self.resize_handle_size))

            if self.current_handle:
                self.is_resizing = True
                self.start_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.is_resizing:
            dx = event.pos().x() - self.start_mouse_pos.x()
            dy = event.pos().y() - self.start_mouse_pos.y()
            if self.current_handle:
                for (hx, hy) in self.current_handle:
                    if hx == 0 and hy == 0:
                        new_width = self.width() - dx
                        new_height = self.height() - dy
                        if new_width > 0 and new_height > 0:
                            self.setFixedSize(new_width, new_height)
                            self.move(self.x() + dx, self.y() + dy)
                            break
                    elif hx == self.width() - self.resize_handle_size and hy == 0:
                        new_width = self.width() + dx
                        if new_width > 0:
                            self.setFixedSize(new_width, self.height())
                            break
                    elif hx == 0 and hy == self.height() - self.resize_handle_size:
                        new_height = self.height() + dy
                        if new_height > 0:
                            self.setFixedSize(self.width(), new_height)
                            break
                    elif hx == self.width() - self.resize_handle_size and hy == self.height() - self.resize_handle_size:
                        new_width = self.width() + dx
                        new_height = self.height() + dy
                        if new_width > 0 and new_height > 0:
                            self.setFixedSize(new_width, new_height)
                            break
            self.start_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_resizing:
            self.is_resizing = False
            self.current_handle = None
            self.update()

    def _is_near_corner(self, pos, x, y):
        return QRect(x, y, self.resize_handle_size, self.resize_handle_size).contains(pos)


class MyTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mime = event.mimeData()
        if mime.hasUrls():
            for url in mime.urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    self.insert_image(file_path)
                else:
                    with open(file_path, "r", encoding="utf-8") as file:
                        self.insertPlainText(file.read())
            event.acceptProposedAction()

    def insert_image(self, file_path):
        self.insertHtml(f'<img src="{file_path}" style="display: block; margin: 0 auto;">')
        self.append("")

    def context_menu(self, position):
        cursor = self.cursorForPosition(position)
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        if not cursor.hasSelection():
            return

        selected_html = cursor.selection().toHtml()
        if '<img' in selected_html:
            menu = self.createStandardContextMenu()
            crop_action = QAction("Resize Image", self)
            crop_action.triggered.connect(self.resize_image)
            menu.addAction(crop_action)
            menu.exec(self.mapToGlobal(position))

    def resize_image(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        selected_html = cursor.selection().toHtml()
        image_path = None

        if '<img' in selected_html:
            start_index = selected_html.find('src="') + 5
            end_index = selected_html.find('"', start_index)
            image_path = selected_html[start_index:end_index]

        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            resizable_image_label = ResizableImageLabel(pixmap)
            resizable_image_label.setWindowTitle("Resize Image")
            resizable_image_label.show()


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Notepad with AI Features")
        self.setGeometry(100, 100, 900, 600)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.add_new_tab_button()

        self.create_menu()

        self.new_tab()
        self.dark_mode = False

    def add_new_tab_button(self):
        self.new_tab_button = QToolButton()
        self.new_tab_button.setText("+")
        self.new_tab_button.clicked.connect(self.new_tab)
        self.tabs.setCornerWidget(self.new_tab_button)

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        text_menu = menu_bar.addMenu("Font")
        features_menu = menu_bar.addMenu("Features")

        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")  # Set shortcut as a string
        new_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")  # Set shortcut as a string
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")  # Set shortcut as a string
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut("Ctrl+Shift+S")  # Set shortcut as a string
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")  # Set shortcut as a string
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")  # Set shortcut as a string
        cut_action.triggered.connect(self.cut_text)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")  # Set shortcut as a string
        copy_action.triggered.connect(self.copy_text)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")  # Set shortcut as a string
        paste_action.triggered.connect(self.paste_content)
        edit_menu.addAction(paste_action)

        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut("Ctrl+A")  # Set shortcut as a string
        select_all_action.triggered.connect(self.select_all_text)
        edit_menu.addAction(select_all_action)

        find_action = QAction("Find", self)
        find_action.setShortcut("Ctrl+F")  # Set shortcut as a string
        find_action.triggered.connect(self.find_text)
        edit_menu.addAction(find_action)

        replace_action = QAction("Replace", self)
        replace_action.setShortcut("Ctrl+R")  # Set shortcut as a string
        replace_action.triggered.connect(self.replace_text)
        edit_menu.addAction(replace_action)

        # Text Menu
        font_action = QAction("Font", self)
        font_action.triggered.connect(self.font_text)
        text_menu.addAction(font_action)

        # Features Menu
        theme_toggle_action = QAction("Toggle Dark/Light Theme", self)
        theme_toggle_action.triggered.connect(self.toggle_theme)
        features_menu.addAction(theme_toggle_action)

        text_to_speech_action = QAction("Text to Speech", self)
        text_to_speech_action.triggered.connect(self.text_to_speech)
        features_menu.addAction(text_to_speech_action)

        speech_to_text_action = QAction("Speech to Text", self)
        speech_to_text_action.triggered.connect(self.speech_to_text)
        features_menu.addAction(speech_to_text_action)

        change_color_action = QAction("Change Text Color", self)
        change_color_action.triggered.connect(self.change_text_color)
        features_menu.addAction(change_color_action)

        insert_hyperlink_action = QAction("Insert Hyperlink", self)
        insert_hyperlink_action.triggered.connect(self.insert_hyperlink)
        features_menu.addAction(insert_hyperlink_action)

    def new_tab(self):
        editor = MyTextEdit()
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(editor)
        tab.setLayout(layout)
        index = self.tabs.addTab(tab, "Untitled")
        self.tabs.setCurrentIndex(index)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")

        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if tab:
                editor = tab.layout().itemAt(0).widget()
                if editor:
                    editor.setStyleSheet("background-color: #1E1E1E; color: white;" if self.dark_mode else
                                         "background-color: white; color: black;")

    def get_current_editor(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            layout = current_tab.layout()
            if layout:
                return layout.itemAt(0).widget()
        return None

    def insert_hyperlink(self):
        editor = self.get_current_editor()
        if editor:
            selected_text = editor.textCursor().selectedText()
            if selected_text:
                url, ok = QInputDialog.getText(self, "Insert Hyperlink", "Enter URL:")
                if ok and url:
                    hyperlink = f'<a href="{url}">{selected_text}</a>'
                    editor.textCursor().insertHtml(hyperlink)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.new_tab()
            editor = self.get_current_editor()
            if editor:
                editor.setText(content)
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(file_path))

    def save_file(self):
        editor = self.get_current_editor()
        if not editor:
            return

        current_index = self.tabs.currentIndex()
        current_tab_name = self.tabs.tabText(current_index)

        if current_tab_name == "Untitled":
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
            if not file_path:
                return
        else:
            file_path = current_tab_name

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(editor.toPlainText())

        self.tabs.setTabText(current_index, os.path.basename(file_path))

    def save_file_as(self):
        editor = self.get_current_editor()
        if not editor:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "",
                                                   "Text Files (*.txt);;All Files (*)")

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(editor.toPlainText())

            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(file_path))

    def close_tab(self, index):
        self.tabs.removeTab(index)

    def cut_text(self):
        editor = self.get_current_editor()
        if editor:
            editor.cut()

    def copy_text(self):
        editor = self.get_current_editor()
        if editor:
            editor.copy()

    def paste_content(self):
        editor = self.get_current_editor()
        if editor:
            editor.paste()

    def select_all_text(self):
        editor = self.get_current_editor()
        if editor:
            editor.selectAll()

    def find_text(self):
        editor = self.get_current_editor()
        if editor:
            text, ok = QInputDialog.getText(self, "Find", "Enter text to find:")
            if ok and text:
                editor.find(text)

    def replace_text(self):
        editor = self.get_current_editor()
        if editor:
            find_text, ok1 = QInputDialog.getText(self, "Replace", "Enter text to find:")
            replace_text, ok2 = QInputDialog.getText(self, "Replace", "Enter text to replace:")
            if ok1 and ok2 and find_text and replace_text:
                editor.setText(editor.toPlainText().replace(find_text, replace_text))

    def font_text(self):
        editor = self.get_current_editor()
        if editor:
            font, ok = QFontDialog.getFont()
            if ok:
                editor.setCurrentFont(font)

    def justify_text(self):
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
            text = cursor.selectedText()
            if text:
                if text.startswith("<p align=\"left\">"):
                    text = text.replace("<p align=\"left\">", "<p align=\"center\">")
                    text = text.replace("</p>", "")
                    text += "</p>"
                elif text.startswith("<p align=\"center\">"):
                    text = text.replace("<p align=\"center\">", "<p align=\"right\">")
                    text = text.replace("</p>", "")
                    text += "</p>"
                elif text.startswith("<p align=\"right\">"):
                    text = text.replace("<p align=\"right\">", "<p align=\"left\">")
                    text = text.replace("</p>", "")
                    text += "</p>"
                else:
                    text = "<p align=\"left\">" + text + "</p>"
                editor.setText(text)

    def change_text_color(self):
        editor = self.get_current_editor()
        if editor:
            color = QColorDialog.getColor()
            if color.isValid():
                editor.setTextColor(color)

    def text_to_speech(self):
        editor = self.get_current_editor()
        if editor:
            text = editor.toPlainText()
            # Add text-to-speech functionality here
            pass

    def speech_to_text(self):
        editor = self.get_current_editor()
        if editor:
            # Add speech-to-text functionality here
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec())