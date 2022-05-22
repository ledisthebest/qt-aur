#!/usr/bin/python

import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QSizePolicy,
    QLabel,
    QMessageBox,
    QMenu,
    QLineEdit,
    QGridLayout,
    QDialogButtonBox
)

from PySide6.QtGui import (
    QIcon,
    QAction    
)


def main():
    app = QApplication(sys.argv)
    win = main_window()
    sys.exit(app.exec())


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # nesting widget in main window to bypass standard layout
        main_ui = QWidget()
        self.setCentralWidget(main_ui)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Loading")
        self.ui_elements(main_ui)

        self.resize(400, 180)
        self.centre()
        self.setWindowTitle(f"AUR Search Tool")
        
        self.menu_items()

        self.show()


    # menubar items
    def menu_items(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menu_file = menubar.addMenu("&File")
        menu_view = menubar.addMenu("&View")
        menu_help = menubar.addMenu("&Help")

        act_quit = QAction(QIcon("exit.png"), "Exit", self)
        act_quit.setShortcut("Ctrl+Q")
        act_quit.setStatusTip("Exit the Program")
        act_quit.triggered.connect(QApplication.instance().quit)

        act_view_stat = QAction("Show Status Bar", self, checkable=True)
        act_view_stat.setStatusTip("Toggle Show/Hide Status Bar")
        act_view_stat.setChecked(True)
        act_view_stat.triggered.connect(self.toggle_statusbar)

        act_about = QAction(QIcon("help.png"), "About", self)
        act_about.setStatusTip("About")
        act_about.triggered.connect(self.about_window)


        menubar = self.menuBar()
        menu_file.addAction(act_quit)
        menu_view.addAction(act_view_stat)
        menu_help.addAction(act_about)


    # center widget
    def ui_elements(self, widget):
        label0 = QLabel("Enter the name or description of the package that you want to search in the Arch User Repository")
        label1 = QLabel("Package Name/Description")
        self.input_line = QLineEdit("Example:brave-browser")
        self.input_line.setMaxLength(50)
        self.input_line.setClearButtonEnabled(True)
        button = QPushButton("Search", self)
        #button.setToolTip("")
        button.resize(button.sizeHint())
        button.clicked.connect(self.get_input)

        layout = QGridLayout()
        layout.setSpacing(20)
        
        layout.addWidget(label0, 0, 1)
        
        layout.addWidget(label1, 1, 0)
        layout.addWidget(self.input_line, 1, 1, 1, 2)

        layout.addWidget(button, 2, 1)

        widget.setLayout(layout)
        self.status_bar.showMessage("Ready")


    def centre(self):
        framesize = self.frameGeometry()
        screen_centre = self.screen().availableGeometry().center()

        framesize.moveCenter(screen_centre)
        self.move(framesize.topLeft())


    # triggered when trying to close window
    def closeEvent(self, event):
        self.statusBar().showMessage("Closing")
        reply = QMessageBox.question(
            self,
            "Comfirm Closing",
            "Are you sure that you want to exit this program?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()

        else:
            self.status_bar.showMessage("Ready")
            event.ignore()


    # override context menu event
    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        act_secret = context_menu.addAction("Easter Egg")

        action = context_menu.exec(self.mapToGlobal(event.pos()))
        if action == act_secret:
            self.status_bar.showMessage("You Found an Easter Egg")


    def toggle_statusbar(self, state):
        if state:
            self.status_bar.show()
        else:
            self.status_bar.hide()


    # about dialog
    def about_window(self):
        QMessageBox.about(
            self,
            "About This Program",
            "A simple AUR search tool, \n written in Qt6 and Python3 \n By: @ledisthebest"
        )

    # lineedit input getter
    def get_input(self):
        return self.input_line.text()


if __name__ == "__main__":
    main()
