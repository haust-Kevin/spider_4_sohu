from Spiders.SpiderBase import SpiderBase
from THEMES_MAP import SCI_THEME_ID_MAP


class SciSpider(SpiderBase):
    URL_PATTERN = 'https://cis.sohu.com/cis/feeds?pvId=1&sceneParam=[{}]'

    def __init__(self, theme: str):
        super().__init__()
        assert theme in SCI_THEME_ID_MAP
        self.__theme = theme

    def _json_url_gene(self):
        param_dict = {
            "page": 0,
            "size": SpiderBase.PAGE_SIZE,
            "spm": "smpc.column-{}.fd-news-1".format(SCI_THEME_ID_MAP[self.__theme])
        }
        while True:
            param_dict['page'] += 1
            yield SciSpider.URL_PATTERN.format(param_dict)

    def _items_of_json(self, json_data):
        return json_data['smpc.column-{}.fd-news-1'.format(SCI_THEME_ID_MAP[self.__theme])]['data']


if __name__ == '__main__':
    spider = SciSpider('5G')
    spider.run()
