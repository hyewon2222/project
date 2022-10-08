import json
import urllib.request

from rest_framework.status import HTTP_200_OK
from project.settings import CLIENT_ID, CLIENT_SECRET


def translation(language, text):
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    parse_text = urllib.parse.quote(text)
    data = f'source=ko&target={language}&text={parse_text}'
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    request = urllib.request.Request(url)
    request.add_header('X-Naver-Client-Id', client_id)
    request.add_header('X-Naver-Client-Secret', client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if (rescode == HTTP_200_OK):
        response_body = response.read()
        translated_text = response_body.decode('utf-8')
        result = json.loads(translated_text)
        return result['message']['result']['translatedText']
    else:
        raise f'Error Code:' + rescode