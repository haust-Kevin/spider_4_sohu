from Spiders.SpiderBase import SpiderBase
from THEMES_MAP import NO_SCI_THEME_ID_MAP


class NosciSpider(SpiderBase):
    URL_PATTERN = 'https://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId={}&page={}&size={}'

    def __init__(self, theme: str):
        super().__init__()
        assert theme in NO_SCI_THEME_ID_MAP
        self.__theme = theme

    def _json_url_gene(self):
        i = 0
        while True:
            i += 1
            yield NosciSpider.URL_PATTERN.format(NO_SCI_THEME_ID_MAP[self.__theme], i, SpiderBase.PAGE_SIZE)


if __name__ == '__main__':
    spider = NosciSpider('互联网')
    spider.run()
