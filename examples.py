#!/usr/bin/python
""" Example usage of iRWebStats """
from ir_webstats import constants as ct
from ir_webstats.client import iRWebStats
from ir_webstats.util import clean
from ir_webstats.util import convertIRMillisToTime

import urllib
import datetime

try:
    import urllib.parse
    encode = urllib.parse.urlencode  # python3
except:
    encode = urllib.urlencode  # python2


user = ''  # iRacing username and password
password = ''
my_leagueid = ''
my_seasonid = ''
my_subsessionid = ''

irw = iRWebStats()
irw.login(user, password)
if not irw.logged:
    print (
        "Couldn't log in to iRacing Membersite. Please check your credentials")
    exit()

# Cars driven by user
r = irw.cars_driven()  # Returns cars id

print("\n--> 1. Cars driven by custid:%s \n" % (irw.custid))
print("\n".join([irw.CARS[c]['name'] for c in r]))

# Career stats
r = irw.career_stats()
print("\n--> 2. Career stats for custid:%s \n" % (irw.custid))
print(("Starts: %s, Wins: %s, Top 5: %s, Total Laps: %s," +
       " Laps Led: %s") % (r['starts'], r['wins'], r['top5'], r['totalLaps'],
                           r['lapsLed']))

#Leagues
r = irw.leagues()
print("\nMy Leagues:")
print("Name | Owner | leagueID")
for leaguerow in r:
    print("%s | %s | %s" % (urllib.unquote_plus(urllib.unquote(leaguerow['leaguename'])), urllib.unquote_plus(urllib.unquote(leaguerow['displayname'])), leaguerow['leagueid']))

#League Seasons
r = irw.league_seasons(my_leagueid)
print("\nLeague seasons for league %s:" % (my_leagueid))
print("Name | SeasonID")
for leaguerow in r:
    print("%s | %s" % (urllib.unquote_plus(urllib.unquote(leaguerow['league_season_name'])), leaguerow['league_season_id']))

#League Results
r = irw.league_season_standings(my_leagueid, my_seasonid)
print("\nLeague Standings for LeagueID %s, SeasonID %s" % (my_leagueid, my_seasonid))
print("\nCar: %s" % (urllib.unquote_plus(urllib.unquote(r['cars'][0]['car_name']))))
print("\nStandings:")
print("Pos | Name | Wins | Avg Start | Avg Finish | Points")
for standingrow in r['standings']['rows']:
    print("%s | %s | %s | %s | %s | %s" %
    (standingrow['pos'], urllib.unquote_plus(urllib.unquote(standingrow['displayname'])), standingrow['wins'], standingrow['avg_start'], standingrow['avg_finish'], standingrow['base_points']))

#League Season sessions
r = irw.league_season_calendar(my_leagueid, my_seasonid)
print("\nLeague Calendar for LeagueID %s, SeasonID %s:" % (my_leagueid, my_seasonid))
print("Date Time | Track | P | Q | R | hasResults | subsessionID")
for calendarrow in r:
    racetime = datetime.datetime.fromtimestamp(calendarrow['launchat']/1000.0)
    print("%s | %s | %sm | %sm | %sm | %s | %s" %
    (racetime, urllib.unquote_plus(urllib.unquote(calendarrow['track_name'])), calendarrow['practicelength'], calendarrow['qualdur'], calendarrow['racelength'], calendarrow['status'] == 4, calendarrow['subsessionid']))

#Subsession results
r = irw.subsession_results(my_subsessionid)
print("\nSubsession results for Subsession %s:" % (my_subsessionid))
print("Pos | Name | Start Pos | Car# | Interval | Laps Led | Fastest Lap Time | League Points")
for resultrow in r['rows']:
    if resultrow['simsesname'] == "RACE": #Valid SimSesNames that I'm aware of are "PRACTICE", "QUALIFY", and "RACE"
        interval = resultrow['interval']
        if interval < 0:
            interval = "-%sL" % (r['eventlapscomplete'] - resultrow['lapscomplete'])
        else:
            interval = convertIRMillisToTime(resultrow['interval'])
            if interval == "0.0":
                interval = ""
            else:
                interval = "-%s" % (interval)

        print("%s | %s | %s | %s | %s | %s | %s | %s" %
        (resultrow['finishpos']+1, urllib.unquote_plus(urllib.unquote(resultrow['displayname'])), resultrow['startpos']+1, resultrow['carnum'], interval, resultrow['lapslead'], convertIRMillisToTime(resultrow['bestlaptime']), resultrow['league_points']))