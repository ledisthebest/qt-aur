import sys
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem


def main():
    bundles = [
        {
            "Description": "bspwm desktop management",
            "FirstSubmitted": 1511058721,
            "LastModified": 1511058722,
            "Maintainer": "cmschuetz",
            "Name": "btops-git",
            "NumVotes": 3,
            "OutOfDate": None,
            "Popularity": 0.000392,
            "URL": "https://github.com/cmschuetz/btops",
            "Version": "0.1.0.r0.g7ecfa08-1",
        },
        {
            "Description": "top-like utility that shows an estimated instantaneous bandwidth on USB buses and devices",
            "FirstSubmitted": 1511819246,
            "LastModified": 1522091983,
            "Maintainer": "zootboy",
            "Name": "usbtop-git",
            "NumVotes": 2,
            "OutOfDate": None,
            "Popularity": 0,
            "URL": "https://github.com/aguinet/usbtop",
            "Version": "0.2-1",
        },
    ]
    app = QApplication()
    print(len(bundles))
    print(len(bundles[0]))

    table = QTableWidget()
    table.setRowCount(len(bundles))
    table.setColumnCount(len(bundles[0]))
    table.setHorizontalHeaderLabels(["Package Name", "Maintainer"])

    for i in range(len(bundles)):
        name = QTableWidgetItem(bundles[i].get("Name"))
        maintainer = QTableWidgetItem(bundles[i]["Maintainer"])
        table.setItem(i, 0, name)
        table.setItem(i, 1, maintainer)

    table.show()
    sys.exit(app.exec())


main()
