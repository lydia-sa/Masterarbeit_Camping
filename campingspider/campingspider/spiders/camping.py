import scrapy

class CampingSpider(scrapy.Spider):
    name = 'camping'
    allowed_domains = ['camping.ch']
    start_urls = ['https://camping.ch/de/campingplaetze']

    # LINKS ABRUFEN
    # -------------------------------------------------------------------
    def parse(self, response):
        # Links von der Übersichtseite extrahieren & sammeln
        links = response.css('div.grid-item-content.items.k0 a::attr(href)').extract()

        # mögliche Duplikate entfernen und wieder in eine Liste gewandelt (für die Einfachere Generierung eines Test-Datensatz).
        unique_links = list(set(links))

        # Test-Datensatz generieren:
        #for link in unique_links[:3]:

        # End-Datensatz:
        for link in unique_links:
            # Link folgen und die Funktion 'parse_websites' ausführen
            # Mit ".follow" können auch relative URLs verwendet werden, ohne sie zu einem absoluten Pfad umzuwandeln
            yield response.follow(url=link, callback=self.parse_campingplatz)

    # ATTRIBUTE ABRUFEN
    # -------------------------------------------------------------------
    def parse_campingplatz(self, response):

        # Sammlung XPaths für gewünschte Attribute:
        feature_xpaths = {
            'Sportplatz': '//*[@id="features"]/div/div[1]/div[3]/div[1]/div/span/span',
            'Golf': '//*[@id="features"]/div/div[1]/div[3]/div[3]/div/span/span',
            'Tennis': '//*[@id="features"]/div/div[1]/div[3]/div[2]/div/span/span',

            'Hallenbad': '//*[@id="features"]/div/div[1]/div[3]/div[7]/div/span/span',
            'Freibad': '//*[@id="features"]/div/div[1]/div[4]/div[11]/div/span/span',
            'Bademöglichkeit': '//*[@id="features"]/div/div[1]/div[4]/div[20]/div/span/span',
            'Babypool': '//*[@id="features"]/div/div[1]/div[4]/div[10]/div/span/span',
            'Bootsvermietung': '//*[@id="features"]/div/div[5]/div[3]/div[7]/div/span/span',
            'Fahrradvermietung': '//*[@id="features"]/div/div[5]/div[3]/div[6]/div/span/span',
            'Unterhaltungsprogramm': '//*[@id="features"]/div/div[1]/div[4]/div[8]/div/span/span',
            'Spielplatz': '//*[@id="features"]/div/div[1]/div[4]/div[9]/div/span/span',
            'Disco': '//*[@id="features"]/div/div[1]/div[4]/div[19]/div/span/span',
            'Wifi': '//*[@id="features"]/div/div[3]/div[1]/div[1]/div/span/span',
            'Aufenthaltsraum': '//*[@id="features"]/div/div[3]/div[5]/div[1]/div/span/span',

            'Informationsstelle': '//*[@id="features"]/div/div[3]/div[5]/div[3]/div/span/span',
            'Behindertengerechter Zugang': '/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/div/span/span',
            'Haustierfreundlichkeit': '/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[7]/div/span/span',
            'Gemeinschaftsküche': '//*[@id="features"]/div/div[3]/div[2]/div[1]/div/span/span',
            'Grillplatz': '//*[@id="features"]/div/div[3]/div[2]/div[2]/div/span/span',

            'Restaurant': '//*[@id="features"]/div/div[1]/div[1]/div[1]/div/span/span',
            'Take away': '//*[@id="features"]/div/div[1]/div[1]/div[2]/div/span/span',
            'Laden mit einfachem Angebot': '//*[@id="features"]/div/div[1]/div[2]/div[1]/div/span/span',
            'Kiosk': '//*[@id="features"]/div/div[1]/div[2]/div[2]/div/span/span',
            'Einkaufzentrum': '//*[@id="features"]/div/div[1]/div[2]/div[4]/div/span/span',
            'Laden mit reichem Angebot': '//*[@id="features"]/div/div[1]/div[2]/div[5]/div/span/span',
            'Waschmaschine': '//*[@id="features"]/div/div[3]/div[4]/div[2]/div/span/span',
            'Trockner': '//*[@id="features"]/div/div[3]/div[4]/div[3]/div/span/span',

            'Wandern': '//*[@id="features"]/div/div[2]/div[4]/div[20]/div/span/span',
            'See mit Kies- oder Sandstrand': '//*[@id="features"]/div/div[4]/div[3]/div[1]/div/span/span',
            'See mit Steinstrand': '//*[@id="features"]/div/div[4]/div[3]/div[2]/div/span/span',
            'Fluss': '//*[@id="features"]/div/div[4]/div[3]/div[3]/div/span/span',

            'Bahnhof': '//*[@id="features"]/div/div[5]/div[2]/div[1]/div/span/span',
            'Busstation': '//*[@id="features"]/div/div[5]/div[2]/div[2]/div/span/span',

            'VSC membership': '/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[4]/div[1]/div/span/span',
            'TCS membership': '/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[4]/div[2]/div/span/span',
            'SCCV membership': '/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[4]/div[3]/div/span/span'
        }

        # Farbe und Text aus Xpath Element extrahieren. Farbe 'lightgrey' gibt Auskunft darüber, dass dieses Merkmal (Feature-Element) nicht angeboten wird.
        # Text wird extrahiert, damit überprüft werden kann, ob das richtige Xpath Element abgerufen wurde.
        def extract_feature_text_and_status(feature_xpath):
            feature = response.xpath(feature_xpath)
            style = feature.xpath('./@style').get()
            text = feature.xpath('normalize-space()').get()
            # wenn die Schrift hellgrau ist, ist das Merkmal nicht vorhanden (0), ansonsten ist es vorhanden (1)
            return 0 if 'lightgrey' in style else 1, text

        # Anzahl Aktivitäten:
        activity_fulltext = response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[6]')
        # Elemente zählen, welche die Klasse 'col-xs-12' aufweisen:
        count_activity = len(activity_fulltext.xpath('.//div[contains(@class, "col-xs-12") and contains(@class, "col-md-12")]'))

        # Anzahl Sterne:
        star_div = response.xpath('/html/body/div[4]/div/div/div[2]/div[1]/div[1]/div').get()
        if star_div:
            # alle aufgeführten Sterne
            num_star = star_div.count('fa fa-star')
            # alle Sterne, die nicht ausgefüllt sind
            num_star_o = star_div.count('fa fa-star-o')
            rating = num_star - num_star_o
        else:
            rating = None

        # extrahiere die gewünschten Elemente & übergeben in einen Dictionary:
        result = {
            'URL': response.url,
            'Name': response.xpath('/html/body/div[3]/div/div/div/div/h1/div[1]/div/text()').get(default='Nicht gefunden'),
            'Ortschaft': response.xpath('normalize-space(/html/body/div[4]/div/div/div[2]/div[1]/div[4]/div/text()[2])').get(default='Nicht gefunden'),
            'Website': response.xpath('normalize-space(/html/body/div[4]/div/div/div[2]/div[1]/div[4]/div/a[2])').get(default='Nicht gefunden'),

            'Sternebewertung': rating,
            'Aktivitäten': count_activity,

            'Touristenstellplätze': response.xpath('normalize-space(/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[4]/p)').get(default='Nicht gefunden'),
            'open (seasons 1)': response.xpath('normalize-space(//*[@id="price"]/p[1]/span)').get(default='Nicht gefunden'),
            'open (seasons 2)': response.xpath('normalize-space(//*[@id="price"]/p[2]/span)').get(default='Nicht gefunden'),
            'open (seasons 3)': response.xpath('normalize-space(//*[@id="price"]/p[3]/span)').get(default='Nicht gefunden'),
            'open (seasons 4)': response.xpath('normalize-space(//*[@id="price"]/p[4]/span)').get(default='Nicht gefunden'),
            'open (seasons 5)': response.xpath('normalize-space(//*[@id="price"]/p[5]/span)').get(default='Nicht gefunden'),
            'open (seasons 6)': response.xpath('normalize-space(//*[@id="price"]/p[6]/span)').get(default='Nicht gefunden'),
            'open (seasons 7)': response.xpath('normalize-space(//*[@id="price"]/p[7]/span)').get(default='Nicht gefunden'),
        }

        # Hinzufügen von weiteren Attribute
        for key, xpath in feature_xpaths.items():
            status, text = extract_feature_text_and_status(xpath)

            # für Test-Datensatz
            #result[key] = f"{status} {text}"

            # End-Datensatz:
            result[key] = status


        # Ausgabe des Resultates:
        yield result