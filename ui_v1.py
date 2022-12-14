from asyncio.windows_events import NULL
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui

import api_get
import requests

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

        self.Tuples = 6
        self.tableWidget.item(0, 0).setBackground(QtGui.QColor(255, 100, 100))

    def openCaptureClass(self):
        # search = searchwindow(self.searchtext.toPlainText())
        # search.exec()
        foodname=searchwindow.findChildren(searchwindow,QTextEdit,'S_searchtext')
        print(foodname)
        widget.setCurrentIndex(widget.currentIndex()+1)
        # self.searchtext.setText('')

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
        print("add")
        self.tableWidget.setItem(
            self.Tuples, 0, QTableWidgetItem(str(self.Tuples)))
        self.tableWidget.setItem(
            self.Tuples, 1, QTableWidgetItem(str(self.Tuples)))
        self.Tuples += 1

    def DELFunction(self):
        print("del")
        # DEL 버튼 눌릴 시
        self.Tuples -= 1
        self.tableWidget.takeItem(self.Tuples, 0)
        self.tableWidget.takeItem(self.Tuples, 1)


class searchwindow(QDialog, QWidget, form_searchclass):
    def __init__(self, foodname):
        super(searchwindow, self).__init__()
        self.initUi()
        self.show()
        # API용 변수들
        self.url = 'https://openapi.foodsafetykorea.go.kr/api'
        self.key = '56bdaba970084b289ebc'
        self.foodname = foodname

        self.S_searchtext.setText(self.foodname)
        self.searching()

        self.S_BackBtn.clicked.connect(self.goMainWindow)
        self.S_searchBtn.clicked.connect(self.searching)
        self.S_tableWidget.doubleClicked.connect(self.goRecipeWindow)

    def openCaptureClass(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def openCaptureClass1(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def initUi(self):
        self.setupUi(self)

    def goRecipeWindow(self):
        searchwindow(self.foodname).close()  # 윈도우 숨김
        self.recipe = recipewindow()
        self.recipe.exec()  # recipe 창 닫을 때까지 기다림
        searchwindow(self.foodname).show()  # recipe 창을 닫으면 다시 첫 번째 창이 보여짐

    def goMainWindow(self):
        self.close()  # 클릭시 종료됨.

    def searching(self):
        self.Tuples = 0 # 표 start
        if self.S_searchtext.toPlainText() != '':
            res = requests.get(api_get.getURL(
                self.url, self.key, self.S_searchtext.toPlainText()))
            recipe = res.json()
            for a in recipe['COOKRCP01']['row']:
                self.S_tableWidget.setItem(self.Tuples,0,QTableWidgetItem(a['RCP_NM'])) # 행 열 데이터
                self.Tuples+=1 # 위에부터 표 채우기
        else:
            print("noThing")

    def table_doubleClicked(self):
        row = self.S_tableWidget.currentIndex().row()
        column = self.S_tableWidget.currentIndex().column()
        print(row,column)
        #새 창 생성

class recipewindow(QDialog, QWidget, form_recipeclass):
    def __init__(self):
        super(recipewindow, self).__init__()
        self.initUi()
        self.show()

        self.R_BackBtn.clicked.connect(self.goSearchWindow)

    def openCaptureClass(self):
         widget.setCurrentIndex(widget.currentIndex()-1)

    def initUi(self):
        self.setupUi(self)

    def goSearchWindow(self):
        self.close()  # 클릭시 종료됨.

    def pushinfo(self):
        print(1)



if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    mainWindow = WindowClass()
    # searchWindow = searchwindow(foodname='')
    # recipeWindow = recipewindow()

    # widget = QStackedWidget()
    # widget.addWidget(mainWindow)
    # widget.addWidget(searchWindow)
    # widget.addWidget(recipeWindow)

    # widget.setFixedHeight(479)
    # widget.setFixedWidth(380)
    # widget.show()
    
    mainWindow.show()

    app.exec_()
