import scrapy

class CampingSpider(scrapy.Spider):
    name = 'camping'
    allowed_domains = ['camping.ch']
    start_urls = ['https://camping.ch/de/campingplaetze']

    def parse(self, response):
        # Links von der Übersichtseite extrahieren & sammeln
        links = response.css('div.grid-item-content.items.k0 a::attr(href)').extract()

        # mögliche Duplikate entfernen
        unique_links = set(links)

        for link in unique_links:
            # Link folgen und die Funktion 'parse_websites' ausführen
            # Mit ".follow" können auch relative URLs verwendet werden, ohne sie zu einem absoluten Pfad umzuwandeln
            yield response.follow(url=link, callback=self.parse_campingplatz)

    def parse_campingplatz(self, response):
        # XPaths für gewünschte Attribute:

        # Anzahl Aktivitaeten:
        activity_fulltext = response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[6]')
        # Elemente zählen, welche die Klasse 'col-xs-12' aufweisen:
        count_activity = len(activity_fulltext.xpath('.//div[contains(@class, "col-xs-12") and contains(@class, "col-md-12")]'))

        # Anzahl Sterne:
        star_div = response.xpath('/html/body/div[4]/div/div/div[2]/div[1]/div[1]/div').get()
        if star_div:
            num_star_o = star_div.count('fa fa-star-o')
            rating = 5 - num_star_o
        else:
            rating = None

        #extrahiere die gewünschten Elemente & übergeben in einen Dictionary
        yield {
            'url': response.url,
            'name': response.xpath('/html/body/div[3]/div/div/div/div/h1/div[1]/div/text()').get(default='Nicht gefunden'),
            'locality': response.xpath('/html/body/div[4]/div/div/div[2]/div[1]/div[4]/div/text()[2]').get(default='Nicht gefunden'),
            'website': response.xpath('/html/body/div[4]/div/div/div[2]/div[1]/div[4]/div/a[2]').get(default='Nicht gefunden'),

            'sport field': response.xpath('//*[@id="features"]/div/div[1]/div[3]/div[1]/div/span/span').get(default='Nicht gefunden'),
            'golf': response.xpath('//*[@id="features"]/div/div[1]/div[3]/div[3]/div/span/span').get(default='Nicht gefunden'),
            'tennis': response.xpath('//*[@id="features"]/div/div[1]/div[3]/div[2]/div/span/span').get(default='Nicht gefunden'),

            'indoor swimming pool': response.xpath('//*[@id="features"]/div/div[1]/div[3]/div[7]/div/span/span').get(default='Nicht gefunden'),
            'unheated pool': response.xpath('//*[@id="features"]/div/div[1]/div[4]/div[11]/div/span/span').get(default='Nicht gefunden'),
            'bathing facilities': response.xpath('//*[@id="features"]/div/div[1]/div[4]/div[20]/div/span/span').get(default='Nicht gefunden'),
            'boat rental': response.xpath('//*[@id="features"]/div/div[5]/div[3]/div[7]/div/span/span').get(default='Nicht gefunden'),
            'bike rental': response.xpath('//*[@id="features"]/div/div[5]/div[3]/div[6]/div/span/span').get(default='Nicht gefunden'),
            'entertainment': response.xpath('//*[@id="features"]/div/div[1]/div[4]/div[8]/div/span/span').get(default='Nicht gefunden'),
            'playground': response.xpath('//*[@id="features"]/div/div[1]/div[4]/div[9]/div/span/span').get(default='Nicht gefunden'),
            'dico': response.xpath('//*[@id="features"]/div/div[1]/div[4]/div[19]/div/span/span').get(default='Nicht gefunden'),
            'wifi': response.xpath('//*[@id="features"]/div/div[3]/div[1]/div[1]/div/span/span').get(default='Nicht gefunden'),
            'TV lounge': response.xpath('//*[@id="features"]/div/div[3]/div[5]/div[2]/div/span/span').get(default='Nicht gefunden'),
            
            'tourist pitches': response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[4]/p').get(default='Nicht gefunden'),
            'easy access for disabled people': response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/div/span/span').get(default='Nicht gefunden'),
            'animals allowed': response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[7]/div/span/span').get(default='Nicht gefunden'),
            'kitchen': response.xpath('//*[@id="features"]/div/div[3]/div[2]/div[1]/div/span/span').get(default='Nicht gefunden'),
            'BBQ area': response.xpath('//*[@id="features"]/div/div[3]/div[2]/div[2]/div/span/span').get(default='Nicht gefunden'),
            'open (seasons 1)': response.xpath('//*[@id="price"]/p[1]/span').get(default='Nicht gefunden'),
            'open (seasons 2)': response.xpath('//*[@id="price"]/p[2]/span').get(default='Nicht gefunden'),
            'open (seasons 3)': response.xpath('//*[@id="price"]/p[3]/span').get(default='Nicht gefunden'),
            'restaurant': response.xpath('//*[@id="features"]/div/div[1]/div[1]/div[1]/div/span/span').get(default='Nicht gefunden'),
            'take away': response.xpath('//*[@id="features"]/div/div[1]/div[1]/div[2]/div/span/span').get(default='Nicht gefunden'),
            'Shop with limited range': response.xpath('//*[@id="features"]/div/div[1]/div[2]/div[1]/div/span/span').get(default='Nicht gefunden'),
            'kiosk': response.xpath('//*[@id="features"]/div/div[1]/div[2]/div[2]/div/span/span').get(default='Nicht gefunden'),
            'shopping centre': response.xpath('//*[@id="features"]/div/div[1]/div[2]/div[4]/div/span/span').get(default='Nicht gefunden'),
            'shop with rich range': response.xpath('//*[@id="features"]/div/div[1]/div[2]/div[5]/div/span/span').get(default='Nicht gefunden'),
            'washing machine': response.xpath('//*[@id="features"]/div/div[3]/div[4]/div[2]/div/span/span').get(default='Nicht gefunden'),
            'laundry dryer / tumble dryer': response.xpath('//*[@id="features"]/div/div[3]/div[4]/div[3]/div/span/span').get(default='Nicht gefunden'),
            
            'star category': rating,
            'VSC membership': response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[4]/div[1]/div/span/span').get(default='Nicht gefunden'),
            'TCS membership': response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[4]/div[3]/div/span/span').get(default='Nicht gefunden'),
            'SCCV membership': response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[4]/div[2]/div/span/span').get(default='Nicht gefunden'),
            
            'hiking': response.xpath('//*[@id="features"]/div/div[2]/div[4]/div[20]/div/span/span').get(default='Nicht gefunden'),
            'lake with shingle / sandy beach': response.xpath('//*[@id="features"]/div/div[4]/div[3]/div[1]/div/span/span').get(default='Nicht gefunden'),
            'lake with stony, rocky beach': response.xpath('//*[@id="features"]/div/div[4]/div[3]/div[2]/div/span/span').get(default='Nicht gefunden'),
            'river': response.xpath('//*[@id="features"]/div/div[4]/div[3]/div[3]/div/span/span').get(default='Nicht gefunden'),
            
            'activities': count_activity,
            'train station': response.xpath('//*[@id="features"]/div/div[5]/div[2]/div[1]/div/span/span').get(default='Nicht gefunden'),
            'bus': response.xpath('//*[@id="features"]/div/div[5]/div[2]/div[2]/div/span/span').get(default='Nicht gefunden'),
        }