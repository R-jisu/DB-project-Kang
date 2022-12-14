import requests
import json
# 56bdaba970084b289ebc
# COOKRCP01
# http://openapi.foodsafetykorea.go.kr/api/keyId/serviceId/dataType/startIdx/endIdx

url = 'https://openapi.foodsafetykorea.go.kr/api'
key = '56bdaba970084b289ebc'

def getURL(endpoint, key, ingredient):

    
    url = f"{endpoint}/{key}/COOKRCP01/json/1/100/RCP_PARTS_DTLS={ingredient}"

    #RCP_PARTS_DTLS={ingredient}
    #print(url)
    # res = requests.get(url, headers=header)
    # return res

    return url

# print(getURL(url, key,'�����'))

# res = requests.get(getURL(url, key,'�����'))
# recipe = res.json()
# for a in recipe['COOKRCP01']['row']:
#   print(a['RCP_NM'])