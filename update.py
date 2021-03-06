import json, random, time
import requests
from bs4 import BeautifulSoup as BS
import threading



class Worm:
    def __init__(self):
        self.user_agent = ["Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)", "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36", "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36", "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36", "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36", "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"]
        self.decodetype = "utf-8"
        self.ogs = []
        self.threadPool = []
        self.threadLimiter = threading.BoundedSemaphore(10)

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

    def handle_request(self, url, max_retry_time, timeout):
        try: 
            respon = requests.get(url=url, headers=self.header(), timeout=timeout)
            if respon.content is None: raise Exception(f"respon content is None max_retry_time:{max_retry_time}")
        except Exception as e:
            if max_retry_time >= 0:
                print(f"Retry due to {e}")
                time.sleep(1)
                respon = self.handle_request(url, max_retry_time - 1, timeout)
            else:
                raise ConnectionRefusedError(f"Retried too many times!!! Server refuse connection.\n{e}")
        return respon
    def open_url(self, url, max_retry_time=10, timeout=1):
        return self.handle_request(url, max_retry_time, timeout).content.decode()

# ________________________________________________________________________________________________________________________________
    def autoSearchAltsite(self, novelName):
        methods = [self.searchMethod1, self.searchMethod2, self.searchMethod3]
        for method in methods:
            altsite = method(novelName)
            if altsite!="-1": return altsite
        print("Alt search failed")
        return "autoSearchFailed"
        
    def searchMethod1(self, novelName):
        print("Altsit 1")
        altsite = "-1"
        base = "https://www.biqugee.com"
        request_url = f"https://www.biqugee.com/search.php?q={novelName}"
        respon = self.open_url(request_url)
        try:
            altsite = base + self.BS(respon).find("a",{"cpos":"title","class":"result-game-item-title-link"})["href"]
            return altsite
        except TypeError:
            return altsite

    def searchMethod2(self, novelName):
        print("Altsit 2")
        altsite = "-1"
        base = "https://www.baidu.com"
        request_url = f"https://www.baidu.com/s?wd={novelName}"
        respon = self.open_url(request_url)
        try:
            result = self.BS(respon).find_all("div", attrs={"class":"result-op c-container xpath-log new-pmd"})
            for re in result:
                if re["mu"] is not "null":
                    altsite = re["mu"]
                    break
            return altsite
        except Exception as e:
            return altsite
    
    def searchMethod3(self, novelName, max_retries = 10):
        print("Altsit 3")
        altsite = "-1"
        base = "https://cn.bing.com"
        request_url = f"https://cn.bing.com/search?q={novelName}"
        respon = self.open_url(request_url)
        try:
            result = self.BS(respon).find_all("div", attrs={"li":"b_algo"})
            for re in result:
                if (re.div.a["href"] is not "null") and ("qidian" not in re.div.a["href"]):
                    altsite = re.div.a["href"]
                    break
            return altsite
        except Exception as e:
            if max_retries > 0:
                time.sleep(1)
                altsite = self.searchMethod3(novelName=novelName, max_retries = max_retries-1)
            return altsite
# ________________________________________________________________________________________________________________________________
    def infoPage_Thread(self, url, altsite="404.html", append=True, autoSearchAltsite=True):
        t = threading.Thread(target=self.infoPage, args=(url, altsite, append, autoSearchAltsite, True))
        self.threadPool.append(t)
        self.threadLimiter.acquire()
        t.start()
        
    def infoPage(self, url, altsite="404.html", append=True, autoSearchAltsite=True, thread=False):
        print(f"Start infoPage {url}")
        """
        get info from qidian.com substract from standard header
        :param url: book url(qidian.com)
        :return: return bookinfo if append is False else add info to self.ogs list
        """ 
        content = self.BS(self.open_url(url, max_retry_time=20, timeout=10))
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
            "update_time":time.time(),
        }
        if og["image"].endswith("300"):og["image"] = og["image"][:-3]+"180"
        if altsite== "404.html" and autoSearchAltsite:
            altsite = self.autoSearchAltsite(og["title"])
        og["altsite"]=altsite
        if append:
            self.ogs.append(og)
        else:
            return og
        if thread:
            self.threadLimiter.release()

    def append_info_data(self, bookinfo):
        """
        append book info to json file to storage
        :param bookinfo: og data
        :return: None
        """
        with open("info.json", "r") as f:
            data = json.loads(f.read())
        if bookinfo not in data:
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

    def nameSearch_Thread(self, name, autoPost = True):
        t = threading.Thread(target=self.nameSearch, args=(name, autoPost, True))
        self.threadPool.append(t)
        self.threadLimiter.acquire()
        t.start()

    def nameSearch(self, name, autoPost = True, thread=False):
        print(f"Start Name search {name}")
        base = "https:"
        request_url = f"https://www.qidian.com/soushu/{name}.html"
        respon = self.BS(self.open_url(request_url))
        try:
            infoPage = base + respon.find("li",{"class":"res-book-item"}).find("h2",{"class":"book-info-title"}).a["href"]
        except (TypeError, AttributeError) as e:
            with open("log/search.html", "w") as f:
                f.write(str(respon))
            print(e)
            print("Search None save html file to log/search.html")
            return -1
        if autoPost:
            self.infoPage(infoPage, autoSearchAltsite=True)
        else:
            return infoPage
        if thread:
            self.threadLimiter.release()

    def output(self, append=False):
        assert len(self.ogs) > 0
        if append:
            for og in self.ogs:
                self.append_info_data(og)
        else:
            self.replace_info_data(self.ogs)
    

class webManager:
    def setSelfInfo(self):
         with open("info.json", "r") as f:
            self.info = json.loads(f.read())
    def update(self, mod="from local", ogs=None):
        if mod == "from local":
            self.setSelfInfo()
        elif mod == "from local append":
            self.setSelfInfo()
            for og in ogs:
                if og not in self.info:
                    self.info.append(og)
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
                    ?????????<br>
                    <a href="{og["novel:read_url"]}"><button>{og["url"].split("/")[2]}</button></a>
                    <a href="{og["altsite"]}"><button>{og["altsite"]}</button></a>
                    <a href="https://www.google.com/search?q={og["title"]}" target="_blank"><button>search {og["title"]}</button></a>
                    
                    </div>
                </td>
                </tr>"""
            txt.append(text_replacement)
        with open("template/index.html", "r") as f: temp = str(f.read())
        with open("index.html", "w") as f:
            f.write(temp.replace("replace", "\n".join(txt)))
    def update_from_worm(self, ogs):
        self.update(mod="from worm", ogs=ogs)
    def update_from_local_append(self, ogs):
        self.update(mod="from local append", ogs=ogs)   

class subpages:
    def __init__(self):
        self.ogs = list(json.load(open("info.json", "w")))
        print(self.ogs)

if __name__ == '__main__':
    worm = Worm()
    if True:
        worm.infoPage_Thread("https://book.qidian.com/info/1009480992/", altsite="https://www.biqugee.com/book/18461/") #???????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1021617576/", altsite="https://www.ddyueshu.com/27171_27171574/") #???????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1029006481/", altsite="https://www.biqugee.com/book/49472/") #???????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1025901449/", altsite="https://www.biqugee.com/book/42560/") #?????????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1023867124/", altsite="https://www.biqugee.com/book/39312/") #??????????????????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1016150754/", altsite="https://www.biqugee.com/book/30784/") #???????????????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1015525869/", altsite="https://www.biqugee.com/book/30809/") #???????????????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1013293257/", altsite="https://www.biqugee.com/book/25454/") #????????????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1012284323/", altsite="https://www.biqugee.com/book/22980/") #?????????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1003306811/", altsite="https://www.biqugee.com/book/3600/") #??????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/2718601/", altsite="https://www.biqugee.com/book/1876/") #???????????????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/3681932/", altsite="https://www.biqugee.com/book/15409/") #???????????????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1025263752/", altsite="https://www.biqugee.com/book/41199/") #?????????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1022282526/", altsite="https://www.biqugee.com/book/37421/") #???????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1013887416/") #??????????????????
        worm.infoPage_Thread("https://book.qidian.com/info/1010377389/") #?????????????????????
        worm.nameSearch_Thread("?????????????????????")
        worm.nameSearch_Thread("???????????????")
        worm.nameSearch_Thread("??????????????????")
        worm.nameSearch_Thread("???????????????????????????")
        worm.nameSearch_Thread("???????????????")
        worm.nameSearch_Thread("???????????????")
        worm.nameSearch_Thread("?????????????????????????????????")
        worm.nameSearch_Thread("???????????????????????????")
        worm.nameSearch_Thread("??????????????????")
        worm.nameSearch_Thread("????????????")
        worm.nameSearch_Thread("???????????????")
        worm.nameSearch_Thread("?????????????????????")
        worm.nameSearch_Thread("???????????????")
        worm.nameSearch_Thread("????????????")
    for t in worm.threadPool:t.join() # wait for all thread join
    webManager().update_from_local_append(worm.ogs)
    worm.output(append=True)
