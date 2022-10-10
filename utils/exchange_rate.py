import urllib.request


url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%98%EC%9C%A8'


def exchange_rate():
    page = urllib.request.urlopen(url)
    text = page.read().decode("utf8")
    cnywhere = text.find('<span>중국 <em>CNY</em></span></a></th> <td><span>')
    usdwhere = text.find('<span>미국 <em>USD</em></span></a></th> <td><span>')
    return {
        'china': text[cnywhere + 48:cnywhere + 54],
        'english': text[usdwhere + 48] + text[usdwhere + 50:usdwhere + 56]
    }