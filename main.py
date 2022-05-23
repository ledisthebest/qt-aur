#!/usr/bin/python

from datetime import datetime
import sys
import requests
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
    QDialogButtonBox,
    QTreeWidget,
    QTreeWidgetItem,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtGui import QIcon, QAction, QColor, QIcon


def main():
    app = QApplication(sys.argv)
    win = main_window()
    sys.exit(app.exec())


def search_aur(user_input, win):
    name = user_input.strip()

    win.status_bar.showMessage(f"Searching...")

    response = requests.get(
        "https://aur.archlinux.org/rpc/?v=5&type=search&arg=" + name
    )  # https://wiki.archlinux.org/title/Aurweb_RPC_interface
    o = response.json()

    if o["resultcount"] != 0:
        win.status_bar.showMessage(f"Found total of {o['resultcount']} packages")
        result = json_to_dict(o)
        return result

    else:
        win.status_bar.showMessage("Nothing Found!")
        return None


def json_to_dict(json_obj):
    dict = []

    for result in json_obj["results"]:
        items = {}
        items["Description"] = result["Description"]
        items["FirstSubmitted"] = result["FirstSubmitted"]
        items["LastModified"] = result["LastModified"]
        items["Maintainer"] = result["Maintainer"]
        items["Name"] = result["Name"]
        items["NumVotes"] = result["NumVotes"]
        items["OutOfDate"] = result["OutOfDate"]
        items["Popularity"] = result["Popularity"]
        items["URL"] = result["URL"]
        items["Version"] = result["Version"]
        dict.append(items)

    print(dict)
    return dict


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # nesting widget in main window to bypass standard layout
        main_ui = QWidget()
        self.setCentralWidget(main_ui)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Loading")
        self.ui_elements(main_ui)

        self.setWindowIcon(QIcon("icon.png"))
        self.resize(400, 180)
        self.centre()
        self.setWindowTitle(f"AUR Search Tool")

        self.menu_items()
        self.table = None

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
        label0 = QLabel(
            "Enter the name or description of the package that you want to search in the Arch User Repository"
        )
        label1 = QLabel("Package Name/Description")
        self.input_line = QLineEdit("Example:brave-browser")
        self.input_line.setMaxLength(50)
        self.input_line.setClearButtonEnabled(True)
        self.button = QPushButton("Search", self)
        # self.button.setToolTip("")
        self.button.resize(self.button.sizeHint())
        self.button.clicked.connect(self.get_input)

        layout = QGridLayout()
        layout.setSpacing(20)

        layout.addWidget(label0, 0, 1)

        layout.addWidget(label1, 1, 0)
        layout.addWidget(self.input_line, 1, 1, 1, 2)

        layout.addWidget(self.button, 2, 1, 2, 1)

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
            # close all other top windows
            for window in QApplication.topLevelWidgets():
                window.close()
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
            "A simple AUR search tool, \n written in Qt6 and Python3 \n By: @ledisthebest",
        )

    # lineedit input getter
    def get_input(self):
        self.button.setEnabled(False)
        self.input_line.setEnabled(False)

        result_dict = search_aur(self.input_line.text(), self)
        if not result_dict is None:

            # avoid creating duplicate window
            if self.table is None:
                self.table = table_widget()

            self.table.update_table(result_dict, self.input_line.text())
            self.table.show()

        self.button.setEnabled(True)
        self.input_line.setEnabled(True)


# table object
class table_widget(QTableWidget):
    def __init__(self):
        super().__init__()

        self.resize(1200, 700)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(
            [
                "Package Name",
                "Version",
                "Last Update Time",
                "Maintainer",
                "Description",
                "Upstream URL",
            ]
        )

    def update_table(self, bundles, search):
        self.setWindowTitle(f"Search Results of: {search}")
        self.setRowCount(len(bundles))

        for i in range(len(bundles)):
            name = QTableWidgetItem(bundles[i]["Name"])
            version = QTableWidgetItem(bundles[i]["Version"])
            converted_time = datetime.fromtimestamp(
                bundles[i]["LastModified"]
            )  # convert unix seconds to time and date
            update = QTableWidgetItem(
                converted_time.strftime("%x %X")
            )  # print date and time based on system locale
            maintainer = QTableWidgetItem(bundles[i]["Maintainer"])
            description = QTableWidgetItem(bundles[i]["Description"])
            link = QTableWidgetItem(bundles[i]["URL"])

            # if package is marked out of date
            if not bundles[i]["OutOfDate"] is None:
                version.setBackground(QColor("red"))

            # if package is orphan
            if bundles[i]["Maintainer"] is None:
                maintainer.setBackground(QColor("red"))

            self.setItem(i, 0, name)
            self.setItem(i, 1, version)
            self.setItem(i, 2, update)
            self.setItem(i, 3, maintainer)
            self.setItem(i, 4, description)
            self.setItem(i, 5, link)


if __name__ == "__main__":
    main()
