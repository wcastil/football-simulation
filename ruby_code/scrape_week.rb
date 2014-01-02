require 'rubygems'
require 'bundler/setup'
require 'espn_scraper'
require 'json'


if ESPN.responding?
   puts "ESPN is responding"
end





print "Enter the week: "
weekNum = gets.chomp.to_i
week = ESPN.get_nfl_scores(2013, weekNum)

matchups = Array.new
week.each do |m|
    hm = m[:home_team].swapcase 
    aw = m[:away_team].swapcase
    if m[:away_score] <= m[:home_score]
       matchups << hm
       matchups << aw 
    else
       matchups << aw
       matchups << hm
    end
end
puts matchups.to_json
f = File.open('../data/week'+weekNum.to_s,'w+') 
f.write(matchups.to_json)

    
