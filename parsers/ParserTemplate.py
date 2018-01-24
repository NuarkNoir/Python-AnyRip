class NameOfParser:
	host = ""
	url_pattern = ""
	checker_regexp = ""
	links = []
	
	def __init__(self, url):
		self.url = self._check_url(url)
			
		
	def parse(self):
		url = self.url
		links_list = []
		return links_list
	
	
	def get_links(self):
		l = []
		for elfirst in self.links:
			if "__iter__" in dir(elfirst):
				for elsecond in elfirst:
					l.append(elsecond)
			else:
				l.append(elfirst)
		self.links = l
		return self.links
	
	
	def get_links_count(self):
		return len(self.links)
	
	
	def _check_url(self, url):
		import re
		if not re.match(self.checker_regexp, url):
			raise Exception("Wrong url given! " + self.host + "parser requires '" + self.url_pattern + "' url pattern.")
		return url
