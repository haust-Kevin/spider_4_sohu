from THEMES_MAP import SCI_THEME_ID_MAP, NO_SCI_THEME_ID_MAP
from Spiders.NosciSpider import NosciSpider
from Spiders.SciSpider import SciSpider

THEMES = list(NO_SCI_THEME_ID_MAP.keys()) + list(SCI_THEME_ID_MAP.keys())


# 爬取的主题
# 默认爬取全部主题
# 请在此处添加主题
# 所有主题请参照 THEMES_MAP.py
# THEMES = [
#     '创业投资',
#     'IT数码',
#     '智能硬件',
#     '生活服务',
#     '互联网',
#     '通讯',
#     '科学',
#     '5G'
# ]


def main():
    themes = THEMES
    # 验证主题是否存在
    for theme in themes:
        if theme not in SCI_THEME_ID_MAP and theme not in NO_SCI_THEME_ID_MAP:
            print('主题<', theme, '>不存在')
            return

    for theme in themes:
        if theme in SCI_THEME_ID_MAP:
            SciSpider(theme).run()
        else:
            NosciSpider(theme).run()


if __name__ == '__main__':
    main()
