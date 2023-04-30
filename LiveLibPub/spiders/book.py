import scrapy
from LiveLibPub.spiders import lib
from LiveLibPub.items import Book


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['www.livelib.ru']

    cookie = {
        "__ll_tum":"662613418",
        "__llutmz":"240",
        "__llutmf":"0",
        "_ga":"GA1.2.426077316.1682586915",
        "_gid":"GA1.2.1760576544.1682586915",
        "_ym_uid":"1682586915223789006",
        "_ym_d":"1682586915",
        "tmr_lvid":"1c37b50983049aec4ab48632c1723ab5",
        "tmr_lvidTS":"1682586915854",
        "__ll_fv":"1682586915",
        "_ym_isad":"2",
        "__ll_popup_count_pviews":"regc1_",
        "__ll_ab_mp":"1",
        "__popupmail_showed":"1000",
        "__popupmail_showed_uc":"1",
        "__ll_popup_count_shows":"regc1_mailc1_",
        "__ll_unreg_session":"3a6c3ded3770923ec678f991c5bb6638",
        "__ll_unreg_sessions_count":"2",
        "LiveLibId":"262037675a1420033e3135da2d4d7082",
        "_gat":"1",
        "_ym_visorc":"b",
        "__ll_dvs":"5",
        "ll_asid":"1259305471",
        "__ll_cp":"32",
        "tmr_detect":"0%7C1682608413824",
        "__ll_dv":"1682608421"
    }
    header = {
        "Cache-Control":"max-age=0",
        "Sec-Ch-Ua":'"Chromium";v="103", ".Not/A)Brand";v="99"',
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":"Linux",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site":"none",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-User":"?1",
        "Sec-Fetch-Dest":"document",
        "Accept-Language":"en-US,en;q=0.9",
        "Accept-Encoding":"gzip, deflate"
    }

    def __init__ (self, bookUrl, count, pub):
        super(BookSpider, self).__init__()
        self.bookUrl = bookUrl
        if(type(count)==int):
            self.maxPage = int(count/20)        #Всего книг / книг на странице = количество страниц для парсинга (Но есть нюанс)
        self.curPage = 2                        #Стартовая страница
        self.pub = pub

    def start_requests(self):
        lib.dbInit()
        lib.initDB(self.name)

        yield scrapy.Request(
            url=self.bookUrl,
            cookies=self.cookie,
            headers=self.header,
            callback=self.parse
        )


    def parse(self, response):
                
        for b in response.xpath("//div[@class='brow-data']/div"):

            ans = Book

            ans.name = b.xpath("a[contains(@class, 'brow-book-name')]/text()").get()
            ans.author = b.xpath("a[@class = 'brow-book-author']/text()").get()
            
            ans.genre = "#".join(response.xpath("div[@class='brow-genres']/a/text()").getall())
            ans.publisher = self.pub
            print(ans.name)
            print(ans.author)
            print(ans.genre)
            print(ans.publisher)
            print("\n\n\n")


        if (self.curPage < self.maxPage):
            yield scrapy.Request(
                url=f"{self.bookUrl}/listview/biglist/~{self.curPage}",
                cookies=self.cookie,
                headers=self.header,
                callback=self.parse
            )
            self.curPage += 1 

        
