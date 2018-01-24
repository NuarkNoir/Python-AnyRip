import requests, lxml.html

class DeviantartParser:
	host = "deviantart"
	url_pattern = "[http[s]://]<author>.deviantart.com/gallery/"
	checker_regexp = "(.*?)(\.)(deviantart.com\/gallery\/)(.*)"
	links = []
	__so = "?offset="
	
	def __init__(self, url):
		self.url = self._check_url(url)
		self.requestor = requests.Session()
		self.requestor.cookies = requests.utils.cookiejar_from_dict(dict(agegate_state='1')) 
			
		
	def parse(self):
		url = self.url
		links_list = []

		html = self.requestor.get(url).text
		for link in self.get_detail_pages(html):
			print(link)
			offset = 0
			while True:
				album_page = self.requestor.get(link + "?offset=" + str(offset)).text
				albums_images = self.get_albums_images(album_page)
				if len(albums_images) == 0:
					break
				links_list += [image_link for image_link in albums_images]
				offset += 24

		self.links = links_list
		return links_list
	
	
	def get_links(self):
		for image_link in set(self.links):
			print(image_link)
			image_page = self.requestor.get(image_link).text
			yield self.get_full_image(image_page)
	
	
	def get_links_count(self):
		return len(self.links)
	
	
	def _check_url(self, url):
		import re
		if not re.match(self.checker_regexp, url):
			raise Exception("Wrong url given! " + self.host + "parser requires '" + self.url_pattern + "' url pattern.")
		return url

	def get_detail_pages(self, source):
		root = lxml.html.fromstring(source)
		links = []
		for link in root.cssselect("a.t"):
			links.append(link.attrib['href'])
		return links


	def get_albums_images(self, source):
		root = lxml.html.fromstring(source)
		links = []
		folderview_art = root.cssselect("div.folderview-art")[0]
		for link in root.cssselect("span.thumb a.torpedo-thumb-link"):
			links.append(link.attrib["href"])
		return links


	def get_full_image(self, source):
		root = lxml.html.fromstring(source)
		main_content = root.cssselect(".dev-view-main-content")[0]
		prev_img = main_content.cssselect("img.dev-content-full")[0].attrib["src"]
		
		meta_content = root.cssselect(".dev-view-meta .dev-view-meta-content")[0]
		meta_actions = meta_content.cssselect(".dev-meta-actions")[0]
		try:
			dp_link = meta_actions.cssselect("a.dev-page-download")[0]
			full_image = self.requestor.get(dp_link.attrib["href"])
			return full_image.url
		except Exception as e:
			print(e.args)
			return prev_img
		



# https://www.deviantart.com/download/721057806/margarita_ferguson_by_kasidesi-dbxarri.png?token=21a8bcec603b72b8cdf82d49083cb3c2712da2fa&ts=1516774545
