from exts.Downloader import Downloader
from parsers.AbstractParser import AbstractParser
from ParsersHub import get_parser

__author__ = "Andrew G aka Nuark Noir"
__copyright__ = "Copyright 2018 Nuark Noir"
__license__ = "Q Public License v1.0"
__maintainer__ = "Nuark Noir"
__email__ = "mrcluster@ya.ru"
__version__ = "0.1-dev"


def main(link, callback=None):
    try:
        parser = get_parser(link)
    except Exception as e:
        print(e)
        return

    assert isinstance(parser, AbstractParser)
    assert issubclass(parser.__class__, AbstractParser)

    if parser.std_many_once:
        print("This parser configured to get all content at once, so it may take many time to do. Please, standby")

    def downloader_callback(x):
        print("Downloading from callback:", x)
        Downloader.download(x, streamy=False)

    parser.parse_range_async(1, 4, inf=False, callback=callback or downloader_callback)


"""
links = ["rariaz", "twigileia", "legendguard", "ofelie"]
for k in links:
    main(f"https://{k}.deviantart.com/gallery/")
"""

main("http://pornreactor.cc/tag/mlp+r34", lambda x: map(print, x) if type(x) == list else print(x))
