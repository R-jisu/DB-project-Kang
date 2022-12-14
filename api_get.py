import requests
import json
# 56bdaba970084b289ebc
# COOKRCP01
# http://openapi.foodsafetykorea.go.kr/api/keyId/serviceId/dataType/startIdx/endIdx

url = 'https://openapi.foodsafetykorea.go.kr/api'

#keyId/serviceId/dataType/startIdx/endIdx
key = '56bdaba970084b289ebc'

def getURL(endpoint, key, ingredient):

    
    url = f"{endpoint}/{key}/COOKRCP01/json/1/5/RCP_PARTS_DTLS={ingredient}"
    
    #RCP_PARTS_DTLS={ingredient}
    #print(url)
    # res = requests.get(url, headers=header)
    # return res

    return url

def get_rcp_URL(endpoint, key, ingredient):

    
    url = f"{endpoint}/{key}/COOKRCP01/json/1/5/RCP_NM={ingredient}"
    
    #RCP_PARTS_DTLS={ingredient}
    #print(url)
    # res = requests.get(url, headers=header)
    # return res

    return url

def get_bar_cd_URL(endpoint, key, barcode):

    
    url = f"{endpoint}/{key}/C005/json/1/1/BAR_CD={barcode}"
    
    #RCP_PARTS_DTLS={ingredient}
    print(url)
    # res = requests.get(url, headers=header)
    # return res

    return url

# print(getURL(url, key,'양배추'))

res = requests.get(get_bar_cd_URL(url, key,'8801056171032'))
# res = requests.get(get_rcp_URL(url, key,'김치찌개'))
# res = requests.get(getURL(url, key,'양배추'))
info = res.json()
print(info)
# for a in info['COOKRCP01']['row']:
#   print(a['RCP_NM'])