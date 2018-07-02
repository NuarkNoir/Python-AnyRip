import os
import shutil
import urllib.parse

import requests


class Downloader:
    @staticmethod
    def escape_filename(string):
        banned_chars = '"<>|:*?\/\n\r\t'
        for char in banned_chars:
            string = string.replace(char, "_")
        return string

    @staticmethod
    def download(link, filename=None, directory="./downloads/", streamy=True, decode=False):
        if not filename:
            filename = link.split("/").pop().split("?")[0]
        else:
            filename = Downloader.escape_filename(filename)
        if not os.path.exists(directory):
            os.mkdir(directory)
        link = Downloader.url_decode(link) if decode else link
        fheaders = requests.head(link)
        try:
            if os.path.exists(directory + filename):
                if os.stat(directory + filename).st_size == int(fheaders.headers["Content-Length"]):
                    return
        except:
            print("Can't read content length D:")
        filereq = requests.get(link, stream=streamy)
        if not filereq.ok:
            return
        with open(directory + filename, "wb") as receive:
            if streamy:
                shutil.copyfileobj(filereq.raw, receive)
            else:
                receive.write(filereq.content)

    @staticmethod
    def url_decode(string):
        return urllib.parse.unquote(urllib.parse.unquote(string))
