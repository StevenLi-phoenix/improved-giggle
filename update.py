import requests
import json, atexit, random, time, os
import requests
from bs4 import BeautifulSoup as BS



class Worm:
    def __init__(self):
        self.user_agent = ["Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)", "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36", "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36", "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36", "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36", "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"]
        self.decodetype = "utf-8"

    def BS(self, content):
        """
        convert content to html parser
        :param content: String
        :return: String
        """
        return BS(content, "html.parser")

    def header(self):
        """
        Select an header with random UA
        :return: String
        """
        headers = {
            "user-agent": random.choice(self.user_agent),
        }
        return headers

    def open_url(self, url, max_retry_time=10):
        try: respon = requests.get(url=url, headers=self.header())
        except Exception as e:
            time.sleep(60)
            if max_retry_time >= 0:
                respon = self.open_url(url, max_retry_time - 1)
            else:
                raise ConnectionRefusedError("Retried too many times!!! Server refuse connection.")
        return respon.content.decode()

    def main(self):
        pass

    def infoPage(self, url, altsite=None):
        if altsite==None:
            altsite="404.html"
        content = self.BS(self.open_url(url))
        og = {
            "url":url,
            "type":content.find("meta", {"property":"og:type"})["content"],
            "title": content.find("meta", {"property": "og:title"})["content"],
            "description": content.find("meta", {"property": "og:description"})["content"],
            "image": content.find("meta", {"property": "og:image"})["content"],
            "novel:category":content.find("meta", {"property": "og:novel:category"})["content"],
            "novel:author": content.find("meta", {"property": "og:novel:author"})["content"],
            "novel:book_name": content.find("meta", {"property": "og:novel:book_name"})["content"],
            "novel:read_url": content.find("meta", {"property": "og:novel:read_url"})["content"],
            "novel:status": content.find("meta", {"property": "og:novel:status"})["content"],
            "novel:author_link": content.find("meta", {"property": "og:novel:author_link"})["content"],
            "novel:update_time": content.find("meta", {"property": "og:novel:update_time"})["content"],
            "novel:latest_chapter_name": content.find("meta", {"property": "og:novel:latest_chapter_name"})["content"],
            "novel:latest_chapter_url": content.find("meta", {"property": "og:novel:latest_chapter_url"})["content"],
            "altsite":altsite,
        }
        self.append_info_data(og)

    def append_info_data(self, bookinfo):
        """
        append book info to json file to storage
        :param bookinfo: og data
        :return: None
        """
        with open("info.txt", "a+") as f:
            f.write(json.dumps(bookinfo)+"\n")

class webManager():
    def update(self):
        def d(text):
            return text
        with open("info.txt", "r") as f:
            self.info = f.read().split("\n")[:-1]
        txt = []
        for book in self.info:
            og = json.loads(book)
            text_replacement = f"""<tr>
            <td style="width: 180px;height: 240px;""><div class="zoom"><a href="{og["url"]}">
            <img
                    src="https:{og["image"]}" alt="bookCover"></a></div>
            </td>

            <td style="width:100%;">
                <a href="{og["url"]}">{d(og["novel:book_name"])}</a>
                <div id="book_intro" style="text-align:left;width:100%;height:max-content;">
                    <p>
                        {d(og["description"])}
                    </p>
                </div>
                <div id="links">
                    链接：<br>
                    <a href="{og["novel:read_url"]}"><button>{og["url"].split("/")[2]}</button></a>
                    <a href="{og["altsite"]}"><button>{og["altsite"]}</button></a>
                    </div>
                </td>
                </tr>"""
            txt.append(text_replacement)
        with open("template/index.html", "r") as f: temp = str(f.read())
        with open("index.html", "w") as f:
            f.write(temp.replace("replace", "\n".join(txt)))
if __name__ == '__main__':
    """UpdateList = [
        "https://book.qidian.com/info/1009480992/",
        "https://book.qidian.com/info/1021617576/",
        "https://book.qidian.com/info/1029006481/",
        "https://book.qidian.com/info/1025901449/",
        "https://book.qidian.com/info/1023867124/",
        "https://book.qidian.com/info/1016150754/",
        "https://book.qidian.com/info/1015525869/",
        "https://book.qidian.com/info/1013293257/",
        "https://book.qidian.com/info/1012284323/",
        "https://book.qidian.com/info/1003306811/",
        "https://book.qidian.com/info/2718601/",
        "https://book.qidian.com/info/3681932/",
    ]"""
    """for i in UpdateList:
        Worm().infoPage(i)
        time.sleep(1)"""
    Worm().infoPage("https://book.qidian.com/info/1025263752/", altsite="https://www.biqugee.com/book/41199/")
    Worm().infoPage("https://book.qidian.com/info/1022282526/", altsite="https://www.biqugee.com/book/37421/")
    webManager().update()