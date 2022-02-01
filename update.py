from curses.ascii import alt
import json, random, time
import requests
from bs4 import BeautifulSoup as BS



class Worm:
    def __init__(self):
        self.user_agent = ["Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)", "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36", "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36", "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36", "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36", "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"]
        self.decodetype = "utf-8"
        self.ogs = []

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
            if max_retry_time >= 0:
                time.sleep(5)
                respon = self.open_url(url, max_retry_time - 1)
            else:
                raise ConnectionRefusedError(f"Retried too many times!!! Server refuse connection.\n{e}")
        return respon.content.decode()

    def main(self):
        pass

    def autoSearchAltsite(self, novelName):
        base = "https://www.biqugee.com"
        request_url = f"https://www.biqugee.com/search.php?q={novelName}"
        respon = self.open_url(request_url)
        try:
            altsite = base + self.BS(respon).find("a",{"cpos":"title","class":"result-game-item-title-link"})["href"]
        except TypeError:
            altsite = "autoSearchFailed"
        return altsite
    
    def infoPage(self, url, altsite="404.html", append=True, autoSearchAltsite=True):
        """
        get info from qidian.com substract from standard header
        :param url: book url(qidian.com)
        :return: return bookinfo if append is False else add info to self.ogs list
        """
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
        }
        if altsite==None and autoSearchAltsite == True:
            altsite = self.autoSearchAltsite(og["title"])
        og["altsite"]=altsite
        if append:
            self.ogs.append(og)
        else:
            return og

    def append_info_data(self, bookinfo):
        """
        append book info to json file to storage
        :param bookinfo: og data
        :return: None
        """
        with open("info.json", "r") as f:
            data = json.loads(f.read())
        data.append(bookinfo)
        with open("info.json", "w") as f:
            f.write(json.dumps(data))

    def replace_info_data(self, bookinfos):
        """
        replace content in info.json
        :param bookinfo: og datas
        :return: None
        """
        with open("info.json", "w") as f:
            f.write(json.dumps(bookinfos))

    def output(self):
        assert len(self.ogs) > 0
        self.replace_info_data(self.ogs)


class webManager():
    def setSelfInfo(self):
         with open("info.json", "r") as f:
            self.info = json.loads(f.read())
    def update(self, mod="from local", ogs=None):
        if mod == "from local":
            self.setSelfInfo()
        elif mod == "from worm":
            self.info = ogs
        txt = []
        for og in self.info:
            text_replacement = f"""<tr>
            <td style="width: 180px;height: 240px;""><div class="zoom"><a href="{og["url"]}">
            <img
                    src="https:{og["image"]}" alt="bookCover"></a></div>
            </td>

            <td style="width:100%;">
                <a href="{og["url"]}">{og["novel:book_name"]}</a>
                <div id="book_intro" style="text-align:left;width:100%;height:max-content;">
                    <p>
                        {og["description"]}
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
    def update_from_worm(self, ogs):
        self.update(mod="from worm", ogs=ogs)
if __name__ == '__main__':
    worm = Worm()
    worm.infoPage("https://book.qidian.com/info/1009480992/", altsite="https://www.biqugee.com/book/18461/") #超神机械师
    worm.infoPage("https://book.qidian.com/info/1021617576/", altsite="https://www.ddyueshu.com/27171_27171574/") #夜的命名术
    worm.infoPage("https://book.qidian.com/info/1029006481/", altsite="https://www.biqugee.com/book/49472/") #不科学御兽
    worm.infoPage("https://book.qidian.com/info/1025901449/", altsite="https://www.biqugee.com/book/42560/") #我的治愈系游戏
    worm.infoPage("https://book.qidian.com/info/1023867124/", altsite="https://www.biqugee.com/book/39312/") #我家老婆来自一千年前
    worm.infoPage("https://book.qidian.com/info/1016150754/", altsite="https://www.biqugee.com/book/30784/") #亏成首富从游戏开始
    worm.infoPage("https://book.qidian.com/info/1015525869/", altsite="https://www.biqugee.com/book/30809/") #变成血族是什么体验
    worm.infoPage("https://book.qidian.com/info/1013293257/", altsite="https://www.biqugee.com/book/25454/") #舌尖上的霍格沃茨
    worm.infoPage("https://book.qidian.com/info/1012284323/", altsite="https://www.biqugee.com/book/22980/") #我有一座冒险屋
    worm.infoPage("https://book.qidian.com/info/1003306811/", altsite="https://www.biqugee.com/book/3600/") #放开那个女巫
    worm.infoPage("https://book.qidian.com/info/2718601/", altsite="https://www.biqugee.com/book/1876/") #进化的四十六亿重奏
    worm.infoPage("https://book.qidian.com/info/3681932/", altsite="https://www.biqugee.com/book/15409/") #名侦探世界里的巫师
    worm.infoPage("https://book.qidian.com/info/1025263752/", altsite="https://www.biqugee.com/book/41199/") #二进制亡者列车
    worm.infoPage("https://book.qidian.com/info/1022282526/", altsite="https://www.biqugee.com/book/37421/") #全职艺术家
    webManager().update_from_worm(worm.ogs)
    worm.output()
