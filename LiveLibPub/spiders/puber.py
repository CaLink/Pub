import scrapy
from LiveLibPub.spiders import lib
from LiveLibPub.items import Card


class PuberSpider(scrapy.Spider):
    name = 'puber'
    allowed_domains = ['www.livelib.ru']
    
    custom_settings = {"LOG_FILE":"db/log/LiveLibPub.log",'DOWNLOAD_DELAY':0,'ROBOTSTXT_OBEY':False}

    to = "https://www.livelib.ru/publishers/~"
    card = "https://www.livelib.ru"
    page = 1665

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

    def start_requests(self):
        lib.dbInit()
        lib.initDB(self.name)

        yield scrapy.Request(
            url="https://www.livelib.ru/publishers/~1664", #1663 страница сломана. Поэтому нужно перезапускать
            cookies=self.cookie,
            headers=self.header,
            callback=self.parse
        )


    def parse(self, response):
        if (response.xpath("//div[@id='leftside']/p").get()):
            return
        
        for link in response.xpath("//h2/a/@href").getall():
            yield scrapy.Request(
                url=self.card+link,
                cookies=self.cookie,
                headers=self.header,
                callback=self.parsePage
            )            

        yield scrapy.Request(
            url=self.to + str(self.page),
            cookies=self.cookie,
            headers=self.header,
            callback=self.parse
        )
        self.page+=1

    def parsePage(self,response):
        
        ans = Card


        try:
            ans.name = response.xpath("//li[@class='active']/a/text()").get()[1:-1]
        except:
            ans.name = ""
        
        try:
            ans.books = response.xpath("//a[contains(text(),'Книги')]/text()").get()[7:-1]
        except:
            ans.books = ""

        try:
            ans.description = response.xpath("//div[@style='padding-left: 251px;']/p/text()").get()
        except:
            ans.description = ""
        
        try:
            ans.city = response.xpath("//div[@id='leftside']/div/p[not(descendant::*)]/text()").get()
        except:
            ans.city = ""
        
        try:
            ans.lastChange = response.xpath("//p[@class='unnoticeable']/text()").get().split(",")[0].split(":")[1].strip().replace(u'\xa0', ' ')
        except:
            ans.lastChange = ""
        
        try:
            ans.url = response.url
        except:
            ans.url = ""

        try:
            ans.urlBook = self.card + response.xpath("//a[contains(text(),'Книги')]/@href").get()
        except:
            ans.urlBook = ""
        
        try:
            ans.siteUrl = response.xpath("//div[@id='leftside']/div/a/@href").get()
        except:
            ans.siteUrl = ""

        lib.dbADD(self.name,ans)
