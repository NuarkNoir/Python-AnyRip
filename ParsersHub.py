from parsers.DeviantartParser import DeviantartParser
from parsers.ReactorParser import ReactorParser

parsers = [DeviantartParser, ReactorParser]


def parser_controller(link):
	parser_ = None
	for parser in parsers:
		try:
			tmp = parser(link)
			parser_ = tmp
			break
		except:
			continue
	if parser_:
		return parser_
	else:
		raise Exception("No parsers available for this link:", link)
