import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox
from PyQt5 import uic


class AddWidget(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.setWindowTitle("Добавить кофе")
        self.pushButton.clicked.connect(self.btn_handler)

    def btn_handler(self):
        try:
            assert self.name.text() != "" and self.description.text() != ""
            self.parent().add_to_db(self.name.text(), self.desc.value(), int(self.grounded.currentText == "Да"),
                                    self.description.text(), self.price.value(), self.volume.value())
            self.close()
        except Exception:
            pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.db = sqlite3.connect("coffee.sqlite")
        self.show_label_d.setWordWrap(True)
        self.addButton.clicked.connect(self.add_btn_handler)
        self.update_combobox()

    def getting_info(self, name: str):
        cr = self.db.cursor()
        q = f"""SELECT degr_of_roasting, is_ground, description, price, volume FROM coffee WHERE name = \"{name}\""""
        res = cr.execute(q).fetchall()
        return res[0]

    def update_labels(self):
        if self.name_chooser.currentText() != "":
            info = self.getting_info(self.name_chooser.currentText())
            self.show_label_s.setText(f"{info[0]}")
            self.show_label_g.setText("Да" if info[1] else "Нет")
            self.show_label_d.setText(info[2])
            self.show_label_p.setText(f"{info[3]}")
            self.show_label_v.setText(f"{info[4]}")

    def add_to_db(self, name, degr_of_roasting: int, is_ground: int, description, price: int, volume: int):
        cr = self.db.cursor()
        q = f"""INSERT INTO coffee(name, degr_of_roasting, is_ground, description, price, volume)
VALUES('{name}', {degr_of_roasting}, {is_ground}, '{description}', {price}, {volume})"""
        cr.execute(q).fetchall()
        self.db.commit()
        self.update_combobox()

    def add_btn_handler(self):
        add_w = AddWidget(self)
        add_w.show()

    def update_combobox(self):
        cr = self.db.cursor()
        dt = list(map(lambda x: x[0], cr.execute("SELECT name FROM coffee")))
        self.name_chooser.clear()
        self.name_chooser.addItems(dt)
        self.name_chooser.currentTextChanged.connect(self.update_labels)
        self.update_labels()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
