from parsers.DeviantArtParser import DeviantArtParser
from parsers.ReactorParser import ReactorParser

parsers = [DeviantArtParser, ReactorParser]


def get_parser(link):
    parser_ = None
    for parser in parsers:
        try:
            tmp = parser(link)
            parser_ = tmp
            break
        except Warning:
            continue
    if parser_:
        return parser_
    else:
        raise Exception("No parsers available for this link:", link)
