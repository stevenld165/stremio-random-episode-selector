import requests
import random
import webbrowser
import imdb
import yaml

globalLink = ''

ia = imdb.Cinemagoer()

#uses imdb api to find the imdb id of the series
def findIMDBid(name):
    movie = ia.search_movie(name)[0]
    return f'tt{movie.movieID}'

# takes season:episode and splits into [season,episode]
def processEpisodeCode(code):
    splitCode = code.split(':')
    separatedCode = []
    for item in splitCode:
        separatedCode.append(item)

    return separatedCode

# reads list, returns list with [showname, episodecode, episodelink, episodename, season#, episode#]
def readListandChooseRandom():
    with open("list.yaml") as seriesListFile:
        seriesList = yaml.safe_load(seriesListFile)['series']

    # choose random show from list first    
    showEntry = random.choice(seriesList)
    showIndex = seriesList.index(showEntry)

    show = seriesList[showIndex]

    seasons = None
    extras = None

    # if the show has extra data, process the data (seasons, extras) otherwise, define name
    if isinstance(show, dict):
        nameOfShow = list(show.keys())[0]

        if 'seasons' in show[nameOfShow].keys():
            seasons = show[nameOfShow]['seasons']

        if 'extra' in show[nameOfShow].keys():
            extras = show[nameOfShow]['extra']
    else:
        nameOfShow = show

    id = findIMDBid(nameOfShow)
    episodeList = []

    # use cinemeta addon api to get the metadata from the imdb id of the show
    r = requests.get(f"https://v3-cinemeta.strem.io/meta/series/{id}.json")
    showMetadata = (r.json())

    #adds episodes to random pool, if seasons are specified, only add episodes from those seasons
    for episode in showMetadata['meta']['videos']:
        if seasons is None:
            episodeList.append(f"{episode['season']}:{episode['number']}")
        elif episode['season'] in range(seasons[0],seasons[1]+1):
            episodeList.append(f"{episode['season']}:{episode['number']}")

    #adds extras if there are any to random episode pool
    if extras is not None:
        for episode in extras:
            episodeList.append(episode)

    finalEpisode = random.choice(episodeList)

    seasonAndEpisodeNumber = processEpisodeCode(finalEpisode)
    
    finalEpisodeName = "Something went wrong"

    #find the name of the episode
    for episode in showMetadata['meta']['videos']:
        if (episode['season'] is int(seasonAndEpisodeNumber[0])) and (episode['number'] is int(seasonAndEpisodeNumber[1])):
            finalEpisodeName = episode['name']
            
    finalLink = f"stremio:///detail/series/{id}/{id}:{finalEpisode}"

    return [nameOfShow, finalEpisode, finalLink, finalEpisodeName, seasonAndEpisodeNumber[0], seasonAndEpisodeNumber[1]]

def roll():
    finalSelection = readListandChooseRandom()

    print(f"Show selected: {finalSelection[0]}")
    print(f"Season: {finalSelection[4]}")
    print(f"Episode: {finalSelection[5]}")
    print(f"Name: {finalSelection[3]} \n")

    global globalLink
    globalLink = finalSelection[2]


print("Stremio Random Episode Chooser\n")
roll()

while True: 
    query = input('Would you like to reroll? (y/n) ') 
    Fl = query[0].lower() 
    if query == '' or not Fl in ['y','n']: 
        print('Please answer with yes or no!') 
    else: 
        if Fl == 'y': 
            print()
            roll()
        if Fl == 'n': 
            webbrowser.open(globalLink)
            break
     

     




