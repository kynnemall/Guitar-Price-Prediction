import scrapy
from ..items import GuitarScraperItem

class ProductInfoSpider(scrapy.Spider):
    name = 'product_info'
    allowed_domains = ['www.thomann.de']
    start_urls = ["https://www.thomann.de/ie/lp_models.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/st_models.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/t_models.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/sg_models.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/semiacoustic_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/heavy_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/jazz_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/fanfret_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/8_string_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/7_string_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/e_guitars_with_piezo_pickups.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/alternative_design_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/signature_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/midi_digital_modelling_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/12_string_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/baritone_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/lefthanded_guitars.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/premium_class.html?ls=25&pg=1",
                  "https://www.thomann.de/ie/shortscale_guitars.html?ls=25&pg=1",
                  ]

    def parse(self, response):
        # check how many products on page
        products = response.css(".fx-product-list-entry::attr(href)").extract()
        if len(products) > 1:
            for p in products:
                p = p.split("?")[0]
                yield response.follow(p, self.parse_product)
        
        # check if link is last page of a category
        if len(products) == 25:
            current_num = response.url.split("pg=")[1]
            new_num = int(current_num) + 1
            new_link = response.url.split("pg=")[0] + f"pg={new_num}"
            yield response.follow(new_link, callback=self.parse)
                
    def parse_product(self, response):
        item = GuitarScraperItem()
        
        item["name"] = response.css("h1::text").get()
        item["price"] = response.css(".primary::text").get()
        item["url"] = response.url
        
        features = response.css(".prod-features span::text").extract()
        paragraphs = response.css(".prod::text").extract()
        item["description"] = ". ".join(features + paragraphs)
        
        yield item
