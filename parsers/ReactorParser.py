import lxml.html
import requests
import asyncio
import concurrent.futures

from exts.RequestsRetry import RequestsRetry
from .AbstractParser import AbstractParser


class ReactorParser(AbstractParser):
    host = "reactor.any"
    url_pattern = "[http://](porn|joy|<fandom>.)reactor.cc/[(tag|search|post|<pagenum>|<nothing>)/(<pagenum>|<nothing>)]"
    checker_regexp = "^(https?://)?(.*)\.?(reactor.cc/)((tag|search|post)/(.*)|\d*|$)"
    links = []

    def __init__(self, url):
        super().__init__(url)
        s = requests.Session()
        s.cookies = requests.utils.cookiejar_from_dict(dict(agegate_state='1'))
        s.headers.update(
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"})
        self.requestor = RequestsRetry.init(session=s)

    def parse(self):
        url = self.url
        links_list = []
        parse_page = url.split("/").pop().isdigit()
        if not url.find("/post/") == -1:
            links_list.extend(self.parse_post(url))
        elif parse_page:
            links_list.extend(self.parse_page(url))
        else:
            for lst in self.parse_standart():
                links_list.extend(lst)
        return links_list

    def parse_page(self, url):
        print("Parsing page with url:", url)
        resp = self.requestor.get(url)
        self._parse_html(resp.text)
        parsed_links = list(self._parse_html(resp.text))
        self.links += parsed_links
        return parsed_links

    def parse_standart(self):
        url = self.url
        print(url)
        resp = self.requestor.get(url)
        root = lxml.html.fromstring(resp.text)
        pagenum = int(root.cssselect('div.pagination_expanded span.current')[0].text)
        for i in range(pagenum, 0, -1):
            yield self.parse_page(url + "/" + str(i))

    def parse_range_async(self, start, end, inf=True, callback=None):
        url = self.url + "?catpath=/"

        self.log(inf, "Reactor parser will report you about current parsing state.")

        async def __loop_links_parser():
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                _loop = asyncio.get_event_loop()
                futures = [
                    _loop.run_in_executor(
                        executor,
                        self.requestor.get,
                        f"{url}/{i}"
                    )
                    for i in range(start, end)
                ]
                for response in await asyncio.gather(*futures):
                    _ci = self._parse_html(response.text)
                    self.links.extend(_ci)
                    if callback:
                        callback(_ci)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(__loop_links_parser())

        return self.links

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
