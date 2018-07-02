import lxml.html
import requests
import asyncio
import concurrent.futures

from exts.RequestsRetry import RequestsRetry
from .AbstractParser import AbstractParser


class DeviantArtParser(AbstractParser):
    host = "deviantart"
    url_pattern = "[http[s]://]<author>.deviantart.com/gallery/<nothing>"
    checker_regexp = "^(https?://)?(.*)\.(deviantart\.com/gallery/)$"
    links = []
    std_many_once = True

    def __init__(self, url):
        super().__init__(url)
        s = requests.Session()
        s.cookies = requests.utils.cookiejar_from_dict(dict(agegate_state='1'))
        s.headers.update(
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"})
        self.requestor = RequestsRetry.init(session=s)

    def parse(self, inf=True, callback=None):
        url = self.url + "?catpath=/"

        self.log(inf, "Deviant parser will report you about current parsing state.")
        offset = 0
        _cl = []
        while True:
            album_page = self.requestor.get(f"{url}&offset={offset}").text
            root = lxml.html.fromstring(album_page)
            albums_images = [link.attrib["href"] for link in root.cssselect("a.torpedo-thumb-link")]
            if len(albums_images) == 0:
                break
            _cl.extend([image_link for image_link in albums_images])
            offset += 24
        self.log(inf, f"Got {len(_cl)}")

        _ci = []

        async def __loop_links_parser():
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                _loop = asyncio.get_event_loop()
                futures = [
                    _loop.run_in_executor(
                        executor,
                        self.requestor.get,
                        l
                    )
                    for l in _cl
                ]
                for response in await asyncio.gather(*futures):
                    _root = lxml.html.fromstring(response.text)
                    div_pb = []  # _root.cssselect("a.dev-page-button")
                    # IDK, but full links giv us 404HTTPError when we are trying to use them
                    link = ""
                    if div_pb:
                        link = div_pb[0].attrib["href"]
                        self.log(inf, f"Found main link: {link}")
                    else:
                        img_full = _root.cssselect("img.dev-content-full")
                        if img_full:
                            link = img_full[0].attrib["src"]
                            self.log(inf, f"Main link not found, but got full common: {link}")
                        else:
                            img_preview = _root.cssselect("img.dev-content-normal")
                            if img_preview:
                                link = img_preview[0].attrib["src"]
                                self.log(inf, f"Main link not found, but got preview: {link}")
                    if callable(callback):
                        callback(link)
                    _ci.append(link)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(__loop_links_parser())

        self.links = list(set(_ci))
        return self.links
