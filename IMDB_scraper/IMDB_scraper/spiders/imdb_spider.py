# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0098904/']

    def parse(self, response):
        cast_and_crew = response.css("[href^=\"fullcredits\"]").attrib["href"]
        cast_and_crew = response.urljoin(cast_and_crew)
        yield scrapy.Request(cast_and_crew, callback = self.parse_full_credits)
    
    def parse_full_credits(self, response):
        actors = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        response = response.replace(url = "https://www.imdb.com")

        for actor in actors:
            actor = response.urljoin(actor)
            yield scrapy.Request(actor, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        actor_name = response.css("span.itemprop::text").get()
        filmography = response.css("div.filmo-row")
        movie_or_TV = filmography.css("b a::text").getall()

        for movie_or_TV_name in movie_or_TV:
            yield{
                "actor" : actor_name,
                "movie_or_TV_name" : movie_or_TV_name
            }