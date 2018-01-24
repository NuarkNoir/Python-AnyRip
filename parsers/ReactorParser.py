import requests, lxml.html

class ReactorParser:
	host = "reactor.any"
	url_pattern = "[http://](porn|joy|<fandom>.)reactor.cc/[(tag|search|post|<pagenum>|<nothing>)/(<pagenum>|<nothing>)]"
	checker_regexp = "(.*?)(\.*)(reactor.cc\/)((tag|search|post)(.*)/\d*|\d*|$)"
	links = []
	
	def __init__(self, url):
		self.url = self._check_url(url)
			
		
	def parse(self):
		url = self.url
		links_list = []
		parse_page = url.split("/").pop().isdigit()
		if not url.find("/post/") == -1:
			links_list += self.parse_post(url)
		elif parse_page:
			links_list += self.parse_page(url)
		else:
			for lst in self.parse_standart():
				links_list += lst
		return links_list
	
	
	def get_links(self):
		l = []
		for elfirst in self.links:
			if type(elfirst) == type([]):
				for elsecond in elfirst:
					l.append(elsecond)
			else:
				l.append(elfirst)
		self.links = l
		return self.links
	
	
	def _check_url(self, url):
		import re
		if not re.match(self.checker_regexp, url):
			raise Exception("Wrong url given! " + self.host + "parser requires '" + self.url_pattern + "' url pattern.")
		return url
		
		
	def parse_page(self, url):
		print("Parsing page with url:", url)
		resp = requests.get(url)
		self._parse_html(resp.text)
		parsed_links = list(self._parse_html(resp.text))
		self.links += parsed_links
		return parsed_links
		
	
	def parse_standart(self):
		url = self.url
		print(url)
		resp = requests.get(url)
		root = lxml.html.fromstring(resp.text)
		pagenum = int(root.cssselect('div.pagination_expanded span.current')[0].text)
		for i in range(pagenum, 0, -1):
			yield self.parse_page(url + "/" + str(i))
		
		
	def parse_post(self, url):
		print("Parsing post with url:", url)
		resp = requests.get(url)
		root = lxml.html.fromstring(resp.text)
		parsed_links = []
		for img in root.cssselect(".post_content img"):
			link = img.attrib['src']
			if not "/post/" in link:
				continue
			if img.attrib['src'].find("/full/") == -1:
				link = link.replace("post", "post/full")
			parsed_links.append(link)
		self.links += parsed_links
		return parsed_links
		

	def _parse_html(self, html):
		root = lxml.html.fromstring(html)
		postContainer = root.cssselect('#post_list div.postContainer')
		for post in postContainer:
			imgs = []
			for img in post.cssselect("img"):
				link = img.attrib['src']
				if not "/post/" in link:
					continue
				if img.attrib['src'].find("/full/") == -1:
					link = link.replace("post", "post/full")
				imgs.append(link)
			yield imgs

		
		
		
		
		
