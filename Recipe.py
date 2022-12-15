from PyQt5.QtWidgets import *
from PyQt5 import uic

import api_get
import requests

form_recipeclass = uic.loadUiType("recipe.ui")[0]


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

        self.ingredient.setText(
            info['COOKRCP01']['row'][0]['RCP_PARTS_DTLS'])

        recipe = ""
        finalrecipe = ""
        for idx in range(1, 20):
            if info['COOKRCP01']['row'][0]['MANUAL'+str(idx).zfill(2)]:
                recipe = info['COOKRCP01']['row'][0]['MANUAL' +
                                                     str(idx).zfill(2)]
                new_recipe = recipe.replace('\n', ' ')
                finalrecipe += new_recipe + '\n'

        self.R_textBrowser.setText(finalrecipe)
