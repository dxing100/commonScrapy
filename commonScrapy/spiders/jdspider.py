import scrapy

from commonScrapy.items import JdMobileItem


class JdspiderSpider(scrapy.Spider):
    name = "jdspider"

    def start_requests(self):
        url = "https://search.jd.com/"
        self.pre_url = url + "search?keyword=华为&cid3=655"
        yield scrapy.Request(url=self.pre_url, callback=self.parse)

    def parse(self, response, *args, **kwargs):
        root = "//div[@id='J_goodsList']//li[@class='gl-item']//div/div[1]/a/@href"
        clicks = response.xpath(root).extract()
        for click in clicks:
            url = "https:" + click
            yield scrapy.Request(url=url, callback=self.parse_detail)
        # 中间存在异步加载数据  待处理
        # 是否存在下一页
        next_page = response.xpath(
            "//div[@id='J_bottomPage']//span[@class='p-num']/a[@class='pn-next']/text()").extract()
        if next_page:
            # 当前页
            page_no = response.xpath("//div[@id='J_bottomPage']//a[@class='curr']/text()").extract() + 1
            url = self.pre_url + '&page=' + page_no
            yield response.follow(url, callback=self.parse)

    @staticmethod
    def parse_detail(response):
        item = JdMobileItem()
        listdl = response.xpath("//div[@id='detail']//div[@class='tab-con']"
                                "//div[@class='Ptable']//div[@class='Ptable-item'][1]/dl/dl")
        for index, x in enumerate(listdl):
            dtname = x.xpath("./dt/text()").extract_first()
            if dtname == '入网型号':
                ddname = x.xpath("./dd[2]/text()").extract_first()
                item["model"] = ddname
            if dtname == '机型':
                ddname = x.xpath("./dd/text()").extract_first()
                item["inmodel"] = ddname
        yield item
