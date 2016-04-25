from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from metacritic.items import MetacriticItem
class MetacriticSpider(CrawlSpider):
	name = "metacritic" # Name of the spider, to be used when crawling
	allowed_domains = ["metacritic.com"] # Where the spider is allowed to go
	start_urls = [
		"http://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed"
	]
	
	rules = (
		Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@rel="next"]',)), callback="parse_games", follow= True),
	)
	
	def parse_games(self, response):
		hxs = HtmlXPathSelector(response) # The XPath selector
		main = hxs.select('//div[@id="main"]')
		sites = main.select('.//h3[@class="product_title"]')
		items = []
		for site in sites:
			item = MetacriticItem()
			item['name'] = site.select('a/text()').extract_first()
			item['link'] = site.select('a/@href').extract_first()
			items.append(item)
		return items
