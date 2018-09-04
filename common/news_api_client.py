import requests

from json import loads

NEWS_API_ENDPOINT = "https://newsapi.org/v1/"
# TODO: use your own key.
NEWS_API_KEY = "8306abaedf1244eab9bfaf10a1979001"

ARTICLES_API = "articles"
SOURCES_API = "sources"

BBC_NEWS = 'bbc-news'
CNN = 'cnn'
IGN = 'ign'

DEFAULT_SOURCES = [CNN]

SORT_BY_TOP = 'top'
SORT_BY_LATEST = 'latest'

def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=ARTICLES_API):
    return end_point + api_name

def getNewsFromSources(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {'apiKey':NEWS_API_KEY,
                   'source':source,
                   'sortBy':sortBy}
        response = requests.get(buildUrl(), params=payload)
        res_json = loads(response.content)

        # Extract info from response.
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # Populate news source in each articles.
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])

    return articles
