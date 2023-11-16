import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.db = sqlite3.connect("coffee.sqlite")
        cr = self.db.cursor()
        dt = list(map(lambda x: x[0], cr.execute("SELECT name FROM coffee")))
        self.name_chooser.addItems(dt)
        self.name_chooser.currentTextChanged.connect(self.update_labels)
        self.update_labels()
        self.show_label_d.setWordWrap(True)

    def getting_info(self, name: str):
        cr = self.db.cursor()
        q = f"""SELECT degr_of_roasting, is_ground, description, price, volume FROM coffee WHERE name = \"{name}\""""
        res = cr.execute(q).fetchall()
        return res[0]

    def update_labels(self):
        info = self.getting_info(self.name_chooser.currentText())
        self.show_label_s.setText(f"{info[0]}")
        self.show_label_g.setText("Да" if info[1] else "Нет")
        self.show_label_d.setText(info[2])
        self.show_label_p.setText(f"{info[3]}")
        self.show_label_v.setText(f"{info[4]}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
