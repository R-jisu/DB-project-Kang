import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from datetime import datetime

import Search
import api_get
import requests
import sqlite3


form_mainclass = uic.loadUiType("main.ui")[0]

conn = sqlite3.connect('./nangbuDB.db')
cur = conn.cursor()


class WindowClass(QMainWindow, form_mainclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.search.clicked.connect(self.goSearchWindow)
        self.ADD.clicked.connect(self.ADDFunction)
        self.sortBtn.clicked.connect(self.sorting)
        self.DELETE.clicked.connect(self.DELFunction)
        self.tableWidget.cellDoubleClicked.connect(
            self.showDialog)  # cell 내용이 바뀌었을 때 기능 실행

        # 표의 전체 row 수 저장 (30개)
        self.row_count = self.tableWidget.rowCount()
        self.cur = cur
        self.conn = conn

        self.flag = 0

        self.Tuples = 0
        cur.execute('SELECT * FROM nangbuDB order by Dday')
        for row in cur:
            self.tableWidget.setItem(self.Tuples, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(self.Tuples, 1, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(self.Tuples, 2, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(
                self.Tuples, 3, QTableWidgetItem(row[2]))  # 바코드
            self.Tuples += 1

        self.initializeDday()

    def initializeDday(self):
        for x in range(self.Tuples):
            # 재료를 표에 저장한 상태일 때, 빈 칸이 아닐 때
            if self.tableWidget.item(x, 1).text() != '':
                days = self.tableWidget.item(x, 1).text().split('.')
                if int(days[0]) < datetime.now().year:  # 1년 이상 지남 -> 죽음
                    self.tableWidget.item(x, 0).setBackground(
                        QtGui.QColor(170, 90, 90))
                    self.tableWidget.setItem(x, 1,
                                             QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (dead)'))
                elif int(days[0]) == datetime.now().year:  # 같은 년도일 때
                    if int(days[1]) < datetime.now().month:  # 1달 이상 지남 -> 죽음
                        self.tableWidget.item(x, 0).setBackground(
                            QtGui.QColor(170, 90, 90))
                        self.tableWidget.setItem(x, 1,
                                                 QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (dead)'))
                    elif int(days[1]) == datetime.now().month:  # 같은 달일때
                        if int(days[2]) < datetime.now().day:  # 하루 이상 지남 -> 죽음
                            self.tableWidget.item(x, 0).setBackground(
                                QtGui.QColor(170, 90, 90))
                            self.tableWidget.setItem(x, 1,
                                                     QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (dead)'))
                        elif int(days[2]) >= datetime.now().day:
                            if (int(days[2]) - datetime.now().day) <= 5:  # 5일 이내로 남음, 핑크색
                                self.tableWidget.item(x, 0).setBackground(
                                    QtGui.QColor(255, 170, 170))
                                if (int(days[2]) - datetime.now().day) == 0:
                                    self.tableWidget.setItem(x, 1,
                                                             QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (D-day)'))
                                else:
                                    self.tableWidget.setItem(x, 1,
                                                             QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (D-' + str(int(days[2]) - datetime.now().day) + ')'))

    def sorting(self):
        for i in range(self.Tuples):
            self.tableWidget.takeItem(i, 0)
            self.tableWidget.takeItem(i, 1)
            self.tableWidget.takeItem(i, 2)
            self.tableWidget.takeItem(i, 3)

        self.Tuples = 0
        cur.execute(
            'SELECT * FROM nangbuDB order by Dday')
        for row in cur:
            self.tableWidget.setItem(self.Tuples, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(self.Tuples, 1, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(self.Tuples, 2, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(
                self.Tuples, 3, QTableWidgetItem(row[2]))  # 바코드
            self.Tuples += 1

        self.initializeDday()

    def showDialog(self):
        if self.tableWidget.currentColumn() == 1 and self.tableWidget.item(self.tableWidget.currentRow(), 3):
            text, ok = QInputDialog.getText(self, '유통기한', '0000.00.00로 입력하세요')
            if ok:
                if text == '':
                    self.tableWidget.setItem(
                        self.tableWidget.currentRow(), 1, QTableWidgetItem(text))
                    Tablecode = self.tableWidget.item(
                        self.tableWidget.currentRow(), 3).text()
                    cur.execute(
                        'update nangbuDB set Dday = ? where barcode = ?', (text, Tablecode,))
                    conn.commit()
                    return

                times = text.split('.')
                if len(times) < 3 or len(times) > 3:
                    QMessageBox.information(self, "닫기", "양식이 잘못되었습니다..")
                    return
                else:
                    if len(times[0]) != 4 or len(times[1]) != 2 or len(times[2]) != 2:
                        QMessageBox.information(
                            self, "닫기", "숫자는 0000.00.00 형태로 넣으셔야 합니다")
                    else:
                        if times[0].isdigit() == False or times[1].isdigit() == False or times[2].isdigit() == False:
                            QMessageBox.information(
                                self, "닫기", "날짜에는 숫자만 넣으실 수 있습니다.")
                        else:
                            if int(times[1]) >= 13 or int(times[2]) >= 32:
                                QMessageBox.information(
                                    self, "닫기", "달과 날짜의 입력이 잘못됐습니다.")
                            else:
                                self.tableWidget.setItem(
                                    self.tableWidget.currentRow(), 1, QTableWidgetItem(text))

                                Tablecode = self.tableWidget.item(
                                    self.tableWidget.currentRow(), 3).text()
                                cur.execute(
                                    'update nangbuDB set Dday = ? where barcode = ?', (text, Tablecode,))
                                conn.commit()

                                # 현재 날짜 출력
                                x = self.tableWidget.currentRow()

                                if int(times[0]) < datetime.now().year:  # 1년 이상 지남 -> 죽음
                                    self.tableWidget.item(x, 0).setBackground(
                                        QtGui.QColor(170, 90, 90))
                                    self.tableWidget.setItem(x, 1,
                                                             QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (dead)'))
                                elif int(times[0]) == datetime.now().year:  # 같은 년도일 때
                                    if int(times[1]) < datetime.now().month:  # 1달 이상 지남 -> 죽음
                                        self.tableWidget.item(x, 0).setBackground(
                                            QtGui.QColor(170, 90, 90))
                                        self.tableWidget.setItem(x, 1,
                                                                 QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (dead)'))

                                    elif int(times[1]) == datetime.now().month:  # 같은 달일때
                                        if int(times[2]) < datetime.now().day:  # 하루 이상 지남 -> 죽음
                                            self.tableWidget.item(x, 0).setBackground(
                                                QtGui.QColor(170, 90, 90))
                                            self.tableWidget.setItem(x, 1,
                                                                     QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (dead)'))
                                        elif int(times[2]) >= datetime.now().day:

                                            # 5일 이내로 남음, 핑크색
                                            if (int(times[2]) - datetime.now().day) <= 5:
                                                self.tableWidget.item(x, 0).setBackground(
                                                    QtGui.QColor(255, 170, 170))
                                                if (int(times[2]) - datetime.now().day) == 0:
                                                    self.tableWidget.setItem(x, 1,
                                                                             QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (D-day)'))
                                                else:
                                                    self.tableWidget.setItem(x, 1,
                                                                             QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (D-' + str(int(times[2]) - datetime.now().day) + ')'))
                                            else:
                                                self.tablecolortowhite(x)
                                        else:
                                            self.tablecolortowhite(x)
                                    else:
                                        self.tablecolortowhite(x)
                                else:
                                    self.tablecolortowhite(x)

    def tablecolortowhite(self, x):
        self.tableWidget.item(x, 0).setBackground(
            QtGui.QColor(255, 255, 255))

    def goSearchWindow(self):
        ingredient = self.searchtext.toPlainText().strip('\n')
        if ingredient == '' or ingredient == '재료':  # 재료명을 입력하지 않은 경우
            QMessageBox.information(self, "닫기", "값을 입력해주세요.")
            self.searchtext.setText('')
            return
        else:  # 재료명이 잘못되었을 경우
            res = requests.get(api_get.getURL(
                api_get.url, api_get.key, ingredient))
            recipe = res.json()
            if recipe['COOKRCP01']['total_count'] == '0':
                QMessageBox.information(self, "닫기", "해당 재료의 레시피가 없습니다.")
                self.searchtext.setText('')
                return

        WindowClass().close()  # 메인윈도우 숨김
        self.search = Search.searchwindow(ingredient)
        self.search.exec()  # search 창 닫을 때까지 기다림
        self.searchtext.setText('')
        WindowClass().show()  # search 창을 닫으면 다시 첫 번째 창이 보여짐

    def ADDFunction(self):
        # ADD 버튼 눌릴 시
        if (self.textEdit.toPlainText()):
            # user가 입력한 바코드가 이미 있는 경우
            for idex in range(self.Tuples):
                if self.textEdit.toPlainText() == self.tableWidget.item(idex, 3).text():
                    self.textEdit.setText('')
                    QMessageBox.information(self, "닫기", "이미 입력한 정보입니다.")
                    return
            # 바코드 api
            res = requests.get(api_get.get_bar_cd_URL(
                api_get.url, api_get.key, self.textEdit.toPlainText()))
            info = res.json()

            if info['C005']['total_count'] != '0':
                for a in info['C005']['row']:
                    mydata = (a['PRDLST_NM'], a['POG_DAYCNT'], a['BAR_CD'], '')
                cur.execute('INSERT into nangbuDB VALUES (?,?,?,?);', mydata)
                conn.commit()

                self.tableWidget.setItem(
                    self.Tuples, 0, QTableWidgetItem(a['PRDLST_NM']))
                self.tableWidget.setItem(
                    self.Tuples, 2, QTableWidgetItem(a['POG_DAYCNT']))
                self.tableWidget.setItem(
                    self.Tuples, 3, QTableWidgetItem(a['BAR_CD']))  # 바코드
                self.Tuples += 1
            else:
                QMessageBox.information(self, "닫기", "없는 정보입니다.")
            self.textEdit.setText('')

    def DELFunction(self):
        if self.tableWidget.item(self.tableWidget.currentRow(), 3):
            self.Tuples -= 1
            Tablecode = self.tableWidget.item(
                self.tableWidget.currentRow(), 3).text()
            cur.execute('delete from nangbuDB where barcode = ?', (Tablecode,))
            conn.commit()
            self.tableWidget.removeRow(self.tableWidget.currentRow())


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    # 프로그램 화면을 보여주는 코드
    myWindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
