from PyQt5.QtWidgets import *
from PyQt5 import uic

import api_get
import Recipe
import requests

form_searchclass = uic.loadUiType("search.ui")[0]


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
        searchwindow(self.foodname).close()
        choicefood = self.S_tableWidget.item(
            self.S_tableWidget.currentRow(), 0).text()
        self.recipe = Recipe.recipewindow(foodtitle=choicefood)
        self.recipe.exec()
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
            QMessageBox.information(self, "닫기", "값을 입력해주세요.")
