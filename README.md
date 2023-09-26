# stremio-random-episode-selector
Chooses a random episode from a list of series and opens the episode page in Stremio.

## How to use
Make sure you have the [IMDB Cinemagoer](https://cinemagoer.github.io/) python package installed. Install using `pip install git+https://github.com/cinemagoer/cinemagoer`.

Have **list.yaml** in the same folder as **main.py** and run it however you like.
It will then output a selection from your list, and ask whether or not you would like to reroll the selection.
- type y to reroll and get a new selection
- type n to open the episode in Stremio (opens to series page with the episode already selected, you will have to choose the source for watching whatever that may be)

![image](https://github.com/stevenld165/stremio-random-episode-selector/assets/19599232/78ee4f43-0ef9-4435-881a-c404aaaaf0cf)
![ezgif-3-3b9c1ac4aa](https://github.com/stevenld165/stremio-random-episode-selector/assets/19599232/1d096a26-6e64-4246-8f0f-ace9f838a957)


## list.yaml format
The formatting is simple, inside the series key, add any series you may want to watch. This name does not have to be exact as long as it is close enough and will not be confused with another series.

You can also specify the range of what seasons the script will draw from by typing it as a list of 2 numbers (cannot specify exact seasons only ranges like `[2,4]` for seasons 2 through 4 and `[1,1]` for just season 1)

In addition, you can specify exact episodes to add to the pool the script will draw from by adding it in the extra key. Must be formatted the following way `season#:episode#` and these numbers come from TVDB (good for if you want to add episodes outside your season scope without adding the rest)

Seasons will work without extras, and extras theoretically work without seasons, but I don't know of a scenario in which you would need to specify extras without limiting the season scope. (Not specifying seasons draws from all episodes including season 0's)

Example:
``` yaml
series:
  - show1
  - show2:
    seasons: [2,5]
  - show3:
    seasons: [1,6]
    extra:
      - 7:12
```
This example will choose a random episode from show1, seasons 2-5 of show2, and seasons 1-6 of show3 with its extra as well.
Feel free to use the provided list.yaml file and edit for your needs.

## How it works
The script uses both IMDB's Cinemagoer and [Stremio's Cinemeta Addon Api](https://v3-cinemeta.strem.io/) in order to fufill its duty. 

It reads the list.yaml file and before doing anything else, chooses a random series from the list. Afterwards, it then uses IMDB's Cinemegoer to find the IMDB id of the show using a search (The first result is used). Using this ID, the script uses the Cinemeta API to then find the metadata for the show that has been selected. It adds all of the episodes in a series into a pool of episodes to choose from, and if a season range is specified it only adds episodes from seasons in that range. It also adds any extras specified into the pool. Finally it chooses an episode and creates a stremio link that opens that episode `stemio:///detail/series/imdbid/imdbid:season:episode` and outputs them out to the user.
