import json
import urllib.request

from rest_framework.status import HTTP_200_OK
from project.settings import CLIENT_ID, CLIENT_SECRET, X_NCP_APIGW_API_KEY_ID, X_NCP_APIGW_API_KEY


def translation(language, text):
    parse_text = urllib.parse.quote(text)
    data = f'source=ko&target={language}&text={parse_text}'
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    request = urllib.request.Request(url)
    request.add_header('X-Naver-Client-Id', CLIENT_ID)
    request.add_header('X-Naver-Client-Secret', CLIENT_SECRET)
    request.add_header('X-NCP-APIGW-API-KEY-ID', X_NCP_APIGW_API_KEY_ID)
    request.add_header('X-NCP-APIGW-API-KEY', X_NCP_APIGW_API_KEY)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if (rescode == HTTP_200_OK):
        response_body = response.read()
        translated_text = response_body.decode('utf-8')
        result = json.loads(translated_text)
        return result['message']['result']['translatedText']
    else:
        raise f'Error Code:' + rescode