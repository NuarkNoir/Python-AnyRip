class DeviantartParser:
	host = "deviantart"
	url_pattern = "[http[s]://]<author>.deviantart.com"
	checker_regexp = "(.*?)(\.)(deviantart.com)(.*)"
	
	def __init__(self, url):
		self.url = self._check_url(url)
			
		
	def parse(self):
		return []
	
	
	def _check_url(self, url):
		import re
		if not re.match(self.checker_regexp, url):
			raise Exception("Wrong url given! " + self.host + "parser requires '" + self.url_pattern + "' url pattern.")
		return url