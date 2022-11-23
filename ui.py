import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui

import api_get
import requests


# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("search.ui")[0]
form_mainclass = uic.loadUiType("main.ui")[0]
# 화면을 띄우는데 사용되는 Class 선언


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.search.clicked.connect(self.searching)
        self.goBack.clicked.connect(self.BackButtonPush)

        self.url = 'https://openapi.foodsafetykorea.go.kr/api'
        self.key = '56bdaba970084b289ebc'

        self.Tuples = 6
        self.tableWidget.item(0, 0).setBackground(QtGui.QColor(255, 100, 100))

    def searching(self):

        if self.searchtext.toPlainText() == '':
            print("noThing")
        else:
            print(self.searchtext.toPlainText(), "검색결과 입니다.")

            res = requests.get(api_get.getURL(
                self.url, self.key, self.searchtext.toPlainText()))
            recipe = res.json()
            for a in recipe['COOKRCP01']['row']:
                print(a['RCP_NM'])

    def BackButtonPush(self):
        print("홈화면으로갑니다.")
        self.tableWidget.setItem(
            self.Tuples, 0, QTableWidgetItem(str(self.Tuples)))
        self.tableWidget.setItem(
            self.Tuples, 1, QTableWidgetItem(str(self.Tuples)))
        self.Tuples += 1


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
