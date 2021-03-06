# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy

class LeagueListing(scrapy.Spider):
    name = "leagues"
    url = 'https://www.lequipe.fr'
    start_urls = [
        url+'/Football/',
    ]
    def parse(self, responce):
        for league in responce.css("div.navigation__sousmenu__level.navigation__sousmenu__level--1 ul li a"):
            leagueName = league.css("a::text").extract_first()
            leagueLink = league.css("a::attr(href)").extract_first()
            print leagueName + '->' + leagueLink
            yield responce.follow(url=leagueLink, callback=self.parseTeam)

    def parseTeam(self, responce):
        for team in responce.css("div#liste_club a"):
            teamName = team.css("a::attr(title)").extract_first()
            teamLink = team.css("a::attr(href)").extract_first()
            print teamName + "->" + teamLink
            yield responce.follow(url=teamLink, callback=self.parseStaff)

    def parseStaff(self, responce):
        print "//////////////////////"
        print responce.css("section.fichetitle h1::text").extract_first()
        print "//////////////////////"
        for staff in responce.css("div#EFFECTIF tr td.nom"):
            staffName = staff.css("a::text").extract_first()
            staffLink = staff.css("a::attr(href)").extract_first()
            print "\t" + staffName + '\t->' + staffLink
            yield responce.follow(url=staffLink, callback=self.parsePlayer)

    def parsePlayer(self, responce):
        player = {}
        #Joueur
        player['Name'] = responce.css("section.fichetitle.titlejoueur h1::text").extract_first()
        player['ImgUrl'] = responce.css("section#INFO div.zP_picPlay img::attr(src)").extract_first()

        tabIdentity = []
        for identity in responce.css("section#INFO div.zP_infPlay tr"):
            elem = identity.css("td")
            if len(elem) == 2:
                newElem = elem.css("td::text").extract()
                tabIdentity.append(newElem[-1])
        print str(tabIdentity)
        print str(player)
        #carriere internationnale
        #palmares
