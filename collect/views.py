import feedparser
import ssl
from django.http import JsonResponse


# 뉴스 수집
def collect_news(request, site):
    try:
        if site == 'google':
            url = 'https://news.google.com/rss/search?q=%EC%BD%94%EB%B9%97+when:1d&hl=ko&gl=KR&ceid=KR:ko'
        else:
            raise ValueError

        ssl._create_default_https_context = ssl._create_unverified_context
        rss = feedparser.parse(url)

        print("item: ", rss.entries)

        for item in rss.entries:
            title = item.title
            link = item.link

            print("title:", title, ", link:", link)

        return JsonResponse(status=200, data={'status': 'true', 'message': 'OK'})
    except ValueError:
        return JsonResponse(status=400, data={'status': 'false', 'message': 'Bad request'})