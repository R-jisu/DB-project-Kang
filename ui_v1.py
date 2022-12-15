import re
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from datetime import datetime

import api_get
import requests
import sqlite3


conn = sqlite3.connect('./nangbuDB.db')
cur = conn.cursor()
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_recipeclass = uic.loadUiType("recipe.ui")[0]
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
        # self.tableWidget.cellDoubleClicked.connect(self.Dday) # cell 내용이 바뀌었을 때 기능 실행
        # self.tableWidget.cellChanged.connect(self.Dday)

        self.Tuples = 0

        # 표의 전체 row 수 저장 (30개)
        self.row_count = self.tableWidget.rowCount()

        self.cur = cur
        self.conn = conn

        self.flag = 0

        cur.execute('SELECT * FROM nangbuDB')
        for row in cur:
            self.tableWidget.setItem(self.Tuples, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(self.Tuples, 1, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(self.Tuples, 2, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(
                self.Tuples, 3, QTableWidgetItem(row[2]))  # 바코드
            self.Tuples += 1

        # 현재 날짜 출력
        # print(datetime.now().year,datetime.now().month,datetime.now().day)
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

    # def Dday(self):
    #     print('change')

        # self.tableWidget.currentRow()
        # self.tableWidget.currentColumn()

    def goSearchWindow(self):
        WindowClass().close()  # 메인윈도우 숨김
        self.search = searchwindow(self.searchtext.toPlainText())
        self.search.exec()  # search 창 닫을 때까지 기다림
        self.searchtext.setText('')
        WindowClass().show()  # search 창을 닫으면 다시 첫 번째 창이 보여짐

    def ADDFunction(self):
        # ADD 버튼 눌릴 시
        # self.tableWidget.item(self.tableWidget.currentRow(),self.tableWidget.currentColumn()).text()
        # print(self.tableWidget.item(self.tableWidget.currentRow(),self.tableWidget.currentColumn()).text())
        global url
        global key

        if (self.textEdit.toPlainText()):
            print(self.textEdit.toPlainText())

            # user가 입력한 바코드가 이미 있는 경우
            for idex in range(self.Tuples):
                if self.textEdit.toPlainText() == self.tableWidget.item(idex, 3).text():
                    self.textEdit.setText('')
                    print('이미 입력한 값입니다.')
                    return

            res = requests.get(api_get.get_bar_cd_URL(
                api_get.url, api_get.key, self.textEdit.toPlainText()))
            info = res.json()
            # print(info)

            if info['C005']['total_count'] != '0':
                for a in info['C005']['row']:
                    print(a['PRDLST_NM'])  # 제품 이름
                    print(a['BAR_CD'])  # 바코드
                    print(a['POG_DAYCNT'])  # 제조일자
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
                print("바코드 정보가 없습니다")
            self.textEdit.setText('')

    def DELFunction(self):
        print("del")
        # DEL 버튼 눌릴 시
        self.Tuples -= 1
        # self.tableWidget.takeItem(self.Tuples, 0)
        # self.tableWidget.takeItem(self.Tuples, 1)

        Tablecode = self.tableWidget.item(
            self.tableWidget.currentRow(), 3).text()
        print(Tablecode)

        cur.execute('delete from nangbuDB where barcode = ?', (Tablecode,))
        conn.commit()

        self.tableWidget.removeRow(self.tableWidget.currentRow())
        # self.tableWidget.removeRow(self.tableWidget.currentRow())


class searchwindow(QDialog, QWidget, form_searchclass):
    def __init__(self, foodname):
        super(searchwindow, self).__init__()
        self.initUi()
        self.show()

        self.foodname = foodname

        self.S_searchtext.setText(self.foodname)
        self.searching()

        self.S_BackBtn.clicked.connect(self.goMainWindow)
        self.S_searchBtn.clicked.connect(self.searching)
        self.S_tableWidget.doubleClicked.connect(self.goRecipeWindow)

    def initUi(self):
        self.setupUi(self)

    def goRecipeWindow(self):
        searchwindow(self.foodname).close()  # 윈도우 숨김
        choicefood = self.S_tableWidget.item(
            self.S_tableWidget.currentRow(), 0).text()
        self.recipe = recipewindow(foodtitle=choicefood)
        self.recipe.exec()  # recipe 창 닫을 때까지 기다림
        searchwindow(self.foodname).show()  # recipe 창을 닫으면 다시 첫 번째 창이 보여짐

    def goMainWindow(self):
        self.close()  # 클릭시 종료됨.

    def searching(self):
        self.Tuples = 0  # 표 start
        if self.S_searchtext.toPlainText() != '':
            res = requests.get(api_get.getURL(
                api_get.url, api_get.key, self.S_searchtext.toPlainText()))
            recipe = res.json()
            for a in recipe['COOKRCP01']['row']:
                self.S_tableWidget.setItem(
                    self.Tuples, 0, QTableWidgetItem(a['RCP_NM']))  # 행 열 데이터
                self.Tuples += 1  # 위에부터 표 채우기
        else:
            print("noThing")

    def table_doubleClicked(self):
        row = self.S_tableWidget.currentIndex().row()
        column = self.S_tableWidget.currentIndex().column()
        print(row, column)
        # 새 창 생성


class recipewindow(QDialog, QWidget, form_recipeclass):
    def __init__(self, foodtitle):
        super(recipewindow, self).__init__()
        self.initUi()
        self.show()
        self.foodtitle = foodtitle

        self.pushinfo()
        self.R_BackBtn.clicked.connect(self.goSearchWindow)

    def initUi(self):
        self.setupUi(self)

    def goSearchWindow(self):
        self.close()  # 클릭시 종료됨.

    def pushinfo(self):
        self.title.setText(self.foodtitle)
        # 요리 레시피 info 출력
        res = requests.get(api_get.get_rcp_URL(
            api_get.url, api_get.key, self.foodtitle))
        info = res.json()

        self.ingredient.setText(info['COOKRCP01']['row'][0]['RCP_PARTS_DTLS'])

        recipe = ""
        finalrecipe = ""
        for idx in range(1, 20):
            if info['COOKRCP01']['row'][0]['MANUAL'+str(idx).zfill(2)]:
                recipe = info['COOKRCP01']['row'][0]['MANUAL' +
                                                     str(idx).zfill(2)]
                new_recipe = recipe.replace('\n', ' ')
                finalrecipe += new_recipe + '\n'

        self.R_textBrowser.setText(finalrecipe)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    # 프로그램 화면을 보여주는 코드
    myWindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
