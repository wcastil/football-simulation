require 'nokogiri'
require 'open-uri'
require './espn_scraper'


# "  http://www.footballdb.com/scores.html?lg=NFL&yr=2013&type=reg&wk=15  "

wk = 15
doc = Nokogiri::HTML(open("http://www.footballdb.com/scores.html?lg=NFL&yr=2013&type=reg&wk="+wk))
