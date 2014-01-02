#!/usr/bin/env ruby
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'json'

print  "\nEnter the week number (1 to 17): "
weekNum = gets.chomp;
if(weekNum.to_i <1 || weekNum.to_i > 17)
  puts "Invalid week number - should be a number 1 to 17\n"
end



u = "http://www.nfl.com/schedules/2013/REG"+weekNum.to_s
c = open(u).read

M = Array.new
#print c.scan(/<!--\s(awayAbbr|homeAbbr):\s(\w+)/)
matches = c.scan(/false -->\r\s<!--\sawayAbbr:\s(\w+)\s-->\r\s+<!--\shomeAbbr:\s(\w+)/)
matches.flatten!

i = 0
while i < matches.count
  M << matches[i] if not M.include? matches[i]
  i = i+1
end



f = File.open('../data/week'+weekNum.to_s,'w+') 
f.puts(M.to_json)


