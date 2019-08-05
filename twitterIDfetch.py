import sys
import string
import simplejson
from twython import Twython

#WE WILL USE THE VARIABLES DAY, MONTH, AND YEAR FOR OUR OUTPUT FILE NAME
import datetime
now = datetime.datetime.now()
day=int(now.day)
month=int(now.month)
year=int(now.year)


#FOR OAUTH AUTHENTICATION -- NEEDED TO ACCESS THE TWITTER API
t = Twython(app_key='5dBlAKQreMfde02aWkTwvj3cv', #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret='9s17OqhWmvdhJg50V9H9BljOMzkGycGPtYjiXqFooUbVlnrMLl',
    oauth_token='1003877817719767041-b57g3SFSPcuhFq0uXjtLng56ZZIezC',
    oauth_token_secret='nWv4msdIinp8tbMkQjLN1BxHXQSfeFFFuQgCA3fcUJV2C')
   
#REPLACE WITH YOUR LIST OF TWITTER USER IDS
ids = ("27203714")

#ACCESS THE LOOKUP_USER METHOD OF THE TWITTER API -- GRAB INFO ON UP TO 100 IDS WITH EACH API CALL
#THE VARIABLE USERS IS A JSON FILE WITH DATA ON THE 32 TWITTER USERS LISTED ABOVE
users = t.lookup_user(user_id = ids)

#NAME OUR OUTPUT FILE - %i WILL BE REPLACED BY CURRENT MONTH, DAY, AND YEAR
outfn = "twitter_user_data_%i.%i.%i.txt" % (now.month, now.day, now.year)

#NAMES FOR HEADER ROW IN OUTPUT FILE
fields = ("id screen_name name created_at url followers_count friends_count statuses_count \favourites_count listed_count \contributors_enabled description protected location lang expanded_url".split())

#INITIALIZE OUTPUT FILE AND WRITE HEADER ROW   
outfp = open(outfn, "w")
#outfp.write(string.join(fields, "\t") + "\n")  # header
outfp.write("\t".join(fields) + "\n")  # header

#THE VARIABLE 'USERS' CONTAINS INFORMATION OF THE 32 TWITTER USER IDS LISTED ABOVE
#THIS BLOCK WILL LOOP OVER EACH OF THESE IDS, CREATE VARIABLES, AND OUTPUT TO FILE
for entry in users:
    #CREATE EMPTY DICTIONARY
    r = {}
    for f in fields:
        r[f] = ""
    #ASSIGN VALUE OF 'ID' FIELD IN JSON TO 'ID' FIELD IN OUR DICTIONARY
    r['id'] = entry['id']
    #SAME WITH 'SCREEN_NAME' HERE, AND FOR REST OF THE VARIABLES
    r['screen_name'] = entry['screen_name']
    r['name'] = entry['name']
    r['created_at'] = entry['created_at']
    r['url'] = entry['url']
    r['followers_count'] = entry['followers_count']
    r['friends_count'] = entry['friends_count']
    r['statuses_count'] = entry['statuses_count']
    r['favourites_count'] = entry['favourites_count']
    r['listed_count'] = entry['listed_count']
    r['contributors_enabled'] = entry['contributors_enabled']
    r['description'] = entry['description']
    r['protected'] = entry['protected']
    r['location'] = entry['location']
    r['lang'] = entry['lang']
    #NOT EVERY ID WILL HAVE A 'URL' KEY, SO CHECK FOR ITS EXISTENCE WITH IF CLAUSE
    if 'url' in entry['entities']:
        r['expanded_url'] = entry['entities']['url']['urls'][0]['expanded_url']
    else:
        r['expanded_url'] = ''
    print (r)
    #CREATE EMPTY LIST
   
    lst = []
    
  import os
  import pandas
  s = pd.Series(r)
#==============================================================================
#   R = pd.Dataframe(r)
#==============================================================================
writer = pd.ExcelWriter('output.xlsx')
s.to_excel(writer,'Sheet1')    
writer.save()    
os.getcwd()    
    
    #ADD DATA FOR EACH VARIABLE
#==============================================================================
#     for f in fields:
#         lst.append(unicode(r[f]).replace("\/", "/"))
#     #WRITE ROW WITH DATA IN LIST
#     #outfp.write(string.join(lst, "\t").encode("utf-8") + "\n")
#     outfp.write("\t".join(lst).encode('utf-8') + '\n')
#==============================================================================
