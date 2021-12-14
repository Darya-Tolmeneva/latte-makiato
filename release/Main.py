import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem
from PyQt5 import QtWidgets
import mainwindow
import addEditCoffeeForm


class Main(QWidget, mainwindow.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.click)
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        self.item = ''
        self.initUI()

    def initUI(self):
        con = sqlite3.connect("../data/coffee.sqlite")
        cur = con.cursor()
        self.result = cur.execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(250)
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена, руб", "объем упаковки, г"])
        for i in range(len(self.result)):
            for j in range(7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))

    def cell_was_clicked(self, row, column):
        self.item = (self.tableWidget.item(row, 1).text(), self.tableWidget.item(row, 2).text(),
                     self.tableWidget.item(row, 3).text(), self.tableWidget.item(row, 4).text(), self.tableWidget.item(row, 5).text(),
                     self.tableWidget.item(row, 6).text(),)

    def click(self):
        self.edit = Edit(self.tableWidget, self.result, self.item)
        self.edit.show()
        self.item = ''

class Edit(QWidget, addEditCoffeeForm.Ui_Form):
    def __init__(self, table, cof, items):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.click)
        self.table = table
        self.coff = cof
        self.items = items
        self.initUI()

    def initUI(self):
        if self.items != '':
            self.lineEdit.setText(self.items[0])
            self.lineEdit_2.setText(self.items[1])
            self.lineEdit_3.setText(self.items[2])
            self.lineEdit_4.setText(self.items[4])
            self.lineEdit_5.setText(self.items[5])
            self.textEdit.append(self.items[3])
            self.lineEdit.setReadOnly(True)
            self.items = ''

    def click(self):
        con = sqlite3.connect("../data/coffee.sqlite")
        cur = con.cursor()
        if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text():
            if (self.lineEdit_4.text() and self.lineEdit_4.text().isdigit()) and \
                    (self.lineEdit_5.text() and self.lineEdit_5.text().isdigit()):
                edit = False
                for i in self.coff:
                    if self.lineEdit.text() in i:
                        edit = True
                        break
                if not self.textEdit.toPlainText():
                    text = " "
                else:
                    text = self.textEdit.toPlainText()
                if not edit:
                    cur.execute("""INSERT INTO coffee(name, roasting, format, description, cost, packing) VALUES (?, ?, ?, ?, ?, ?)""",
                                (items := self.lineEdit.text(),
                                 self.lineEdit_2.text(),
                                 self.lineEdit_3.text(),
                                 text,
                                 int(self.lineEdit_4.text()),
                                 int(self.lineEdit_5.text()),))
                else:
                    upd = "UPDATE coffee SET roasting = ?, format = ?, description = ?, cost = ?, packing = ? WHERE name = ?"
                    data = (self.lineEdit_2.text(), self.lineEdit_3.text(), text, int(self.lineEdit_4.text()), int(self.lineEdit_5.text()), self.lineEdit.text())
                    cur.execute(upd, data)
                con.commit()
                self.close()
                self.result = cur.execute("""SELECT * FROM coffee""").fetchall()
                self.table.setRowCount(len(self.result))
                for i in range(len(self.result)):
                    for j in range(7):
                        self.table.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())