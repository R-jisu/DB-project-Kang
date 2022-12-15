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
        self.S_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.S_BackBtn.clicked.connect(self.goMainWindow)
        self.S_searchBtn.clicked.connect(self.searching)
        self.S_tableWidget.doubleClicked.connect(self.goRecipeWindow)

    def initUi(self):
        self.setupUi(self)

    def goRecipeWindow(self):
        choicefood = self.S_tableWidget.item(
            self.S_tableWidget.currentRow(), 0).text()
        # 레시피가 있는 데이터인지 확인
        res = requests.get(api_get.get_rcp_URL(
            api_get.url, api_get.key, choicefood))
        info = res.json()
        if info['COOKRCP01']['total_count'] == '0':
            QMessageBox.information(self, "닫기", "레시피를 준비 중입니다.")
            return

        searchwindow(self.foodname).close()
        self.recipeW = Recipe.recipewindow(foodtitle=choicefood)
        self.recipeW.exec()
        searchwindow(self.foodname).show()  # recipe 창을 닫으면 다시 첫 번째 창이 보여짐

    def goMainWindow(self):
        self.close()  # 클릭시 종료됨.

    def wrongQmessageBox(self, text):
        QMessageBox.information(self, "닫기", text)
        self.S_searchtext.setText('')

    # 재료가 들어가는 요리 리스트 검색
    def searching(self):
        self.Tuples = 0  # 표 start
        ingredient = self.S_searchtext.toPlainText().strip('\n')
        if ingredient != '':
            if len(ingredient) == 1 and (ord(ingredient) > 32 and ord(ingredient) < 127):
                self.wrongQmessageBox("값이 잘못되었습니다.")
                return
            if ingredient == '재료':
                self.wrongQmessageBox("값이 잘못되었습니다.")
                return
            res = requests.get(api_get.getURL(
                api_get.url, api_get.key, ingredient))
            recipe = res.json()
            if recipe['COOKRCP01']['total_count'] == '0':
                self.wrongQmessageBox("해당 재료의 레시피가 없습니다.")
            else:
                for a in recipe['COOKRCP01']['row']:
                    self.S_tableWidget.setItem(
                        self.Tuples, 0, QTableWidgetItem(a['RCP_NM']))  # 행 열 데이터
                    self.Tuples += 1  # 위에부터 표 채우기
        elif ingredient == '':
            self.wrongQmessageBox("값을 입력해주세요.")
