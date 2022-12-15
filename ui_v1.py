import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from datetime import datetime

import api_get
import requests
import sqlite3


con = sqlite3.connect('./nangbuDB.db')
cur = con.cursor()
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_searchclass = uic.loadUiType("search.ui")[0]
form_mainclass = uic.loadUiType("main.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언


class WindowClass(QMainWindow, form_mainclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.search.clicked.connect(self.goSearchWindow)
        self.ADD.clicked.connect(self.ADDFunction)
        self.DELETE.clicked.connect(self.DELFunction)

        self.Tuples = 0
        

        # 표의 전체 row 수 저장 (30개)
        self.row_count = self.tableWidget.rowCount()

        self.cur = cur
        cur.execute('SELECT * FROM nangbuDB')
        for row in cur:
            print(row)

            self.tableWidget.setItem(0, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(0, 2, QTableWidgetItem(row[1]))

        #현재 날짜 출력
        #print(datetime.now().year,datetime.now().month,datetime.now().day)
        # for x in range(self.row_count):
            #print(self.tableWidget.item(0, 1).text(), x)
            # if self.tableWidget.item(x, 1): # 재료를 표에 저장한 상태일 때, 빈 칸이 아닐 때
                
                # days = self.tableWidget.item(x, 1).text().split('.')
                # #print(days[0], days[1], days[2])

                # if int(days[0]) < datetime.now().year: #1년 이상 지남 -> 죽음
                #     self.tableWidget.item(x, 0).setBackground(QtGui.QColor(170, 90, 90))
                #     self.tableWidget.setItem(x, 1,
                #             QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (dead)'))
                # elif int(days[0]) == datetime.now().year: #같은 년도일 때
                #     if int(days[1]) < datetime.now().month: # 1달 이상 지남 -> 죽음
                #         self.tableWidget.item(x, 0).setBackground(QtGui.QColor(170, 90, 90))
                #         self.tableWidget.setItem(x, 1,
                #             QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (dead)'))

                #     elif int(days[1]) == datetime.now().month:# 같은 달일때
                #         if int(days[2]) < datetime.now().day: #하루 이상 지남 -> 죽음
                #             self.tableWidget.item(x, 0).setBackground(QtGui.QColor(170, 90, 90))
                #             self.tableWidget.setItem(x, 1,
                #                 QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (dead)'))
                #         elif int(days[2]) >= datetime.now().day:
                            
                #             if (int(days[2]) - datetime.now().day) <= 5: #5일 이내로 남음, 핑크색
                #                 self.tableWidget.item(x, 0).setBackground(QtGui.QColor(255, 170, 170))
                #                 if (int(days[2]) - datetime.now().day) == 0:
                #                     self.tableWidget.setItem(x, 1,
                #                         QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (D-day)'))
                #                 else:
                #                     self.tableWidget.setItem(x, 1,
                #                         QTableWidgetItem(self.tableWidget.item(x, 1).text() + ' (D-' + str(int(days[2]) - datetime.now().day) + ')'))
        # dksl
        # self.tableWidget.item(0, 0).setBackground(QtGui.QColor(255, 100, 100))

        #self.tableWidget.item(self.tableWidget.currentRow(),self.tableWidget.currentColumn()).text()
        #self.tableWidget.item(0, 0).setBackground(QtGui.QColor(255, 100, 100))

    def goSearchWindow(self):
        self.hide()  # 메인윈도우 숨김
        self.search = searchwindow(self.searchtext.toPlainText())
        self.search.exec()  # search 창 닫을 때까지 기다림
        self.searchtext.setText('')
        self.show()  # search 창을 닫으면 다시 첫 번째 창이 보여짐

    def ADDFunction(self):
        # ADD 버튼 눌릴 시
        # self.tableWidget.item(self.tableWidget.currentRow(),self.tableWidget.currentColumn()).text()
        # print(self.tableWidget.item(self.tableWidget.currentRow(),self.tableWidget.currentColumn()).text())
        input("바코드를 입력하세요 : ")
        res = requests.get(api_get.get_bar_cd_URL(api_get.url, api_get.key, '8801056171032'))
        info = res.json()
        print(info)

        # self.tableWidget.setItem(
        #     self.Tuples, 0, QTableWidgetItem(str(self.Tuples)))
        # self.tableWidget.setItem(
        #     self.Tuples, 1, QTableWidgetItem(str(self.Tuples)))
        # self.Tuples += 1

    def DELFunction(self):
        print("del")
        # DEL 버튼 눌릴 시
        self.Tuples -= 1
        # self.tableWidget.takeItem(self.Tuples, 0)
        # self.tableWidget.takeItem(self.Tuples, 1)
        self.tableWidget.removeRow(self.tableWidget.currentRow())
        # self.tableWidget.removeRow(self.tableWidget.currentRow())


class searchwindow(QDialog, QWidget, form_searchclass):
    def __init__(self, foodname):
        super(searchwindow, self).__init__()
        self.initUi()
        self.show()

        # API용 변수들
        self.url = 'https://openapi.foodsafetykorea.go.kr/api'
        self.key = '56bdaba970084b289ebc'
        self.foodname = foodname

        self.searching()

        self.S_BackBtn.clicked.connect(self.goMainWindow)
        self.S_searchBtn.clicked.connect(self.searching)

    def initUi(self):
        self.setupUi(self)

    def goMainWindow(self):
        self.close()  # 클릭시 종료됨.

    def searching(self):
        self.S_searchtext.setText(self.foodname)
        if self.S_searchtext.toPlainText() == '':
            print("noThing")
        else:
            print(self.S_searchtext.toPlainText(), "검색결과 입니다.")

            res = requests.get(api_get.getURL(
                self.url, self.key, self.S_searchtext.toPlainText()))
            recipe = res.json()
            for a in recipe['COOKRCP01']['row']:
                print(a['RCP_NM'])


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    # 프로그램 화면을 보여주는 코드
    myWindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()