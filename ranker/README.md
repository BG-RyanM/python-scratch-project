# album_ranker

## Purpose

On YouTube, you can find videos that rank the albums by a particular band. Typically, users will also leave comments containing their own ranking lists.

To my mind, the best judges of a band's body of work are the serious fans. If a person is familiar enough with the band's work to be able to rank **all** (or nearly all) of the albums in the catalog, then that person can be considered a serious fan (while a casual one might only know a few albums). Serious fans might not be perfectly objective about how good a particular release is, but they're still able to put the whole set of releases into a best-to-worst order.

This program aggregates a set of fan ranking lists into a single "average" list. It also performs statistical analysis, determining which albums are most underrated, most overrated, most controversial, most agreed-on, etc. Where star rankings are provided, it averages those together and compares them to how professional music critics rate the band's catalog.

Other features:
* Gathers statistics on how different "phases" of a band stack up (maybe they changed their lineup or their sound at some point)
* Compares specified users to the statistically average fans
* Uses K-Means Clustering to determine what "camps" of fans exist (typically, some only like the old stuff, while others embrace the newer releases, too).

This program could easily be adapted for other purposes. Best books by an author? Best movies by a director? Same basic logic.

## Use

Basic use:
```commandline
$ python3 album_ranker.py --file bands/PinkFloydLists.txt
```

The source file begins with a chronological list of the band's albums, like so:
```
# Master List: Pink Floyd

1. Piper at the Gates of Dawn @Psychedelic Years (5)
2. A Saucerful of Secrets @Psychedelic Years (3.5)
3. More @Psychedelic Years (3)
4. Ummagumma @Psychedelic Years (3.5)
5. Atom Heart Mother @Psychedelic Years (3)
6. Meddle @Psychedelic Years (4.5)
7. Obscured by Clouds @Psychedelic Years (3)
etc...
```

You can see the album name (`Piper at the Gates of Dawn`), the phase or phases it belongs to (`Psychedelic Years`), and the star rating from music critics (`(5)`).

After that follows a series of fan rankings, like so:
```
# Jason *

15. Ummagumma
14. Piper at the Gates of Dawn
13. The Endless River
12. More
11. A Saucerful of Secrets
10. A Momentary Lapse of Reason
... (snipped)
3. Obscured by Clouds
2. Animals
1. The Dark Side of the Moon
```

In this case, the user is Jason and his least favorite Pink Floyd album is "Ummagumma". His favorite is "The Dark Side of the Moon". He could have also put his list in the opposite order, starting from `1.` and working down to `15.`. If he hadn't heard all fifteen Pink Floyd studio releases, he could have even left a few off the list, making it run from 1 down to, say, 13. 

Jason hasn't given any star ratings, but he could have, like so:

```
3. Obscured by Clouds (4/5 stars)
2. Animals (9/10)
1. The Dark Side of the Moon (5)
```

All of the above are valid ways to provide a star rating. Similarly, the program isn't too picky about the number starting each line. Any of the following will work:
```
1. The Dark Side of the Moon (5)
01. The Dark Side of the Moon (5)
 1. The Dark Side of the Moon (5)
1) The Dark Side of the Moon (5)
1 The Dark Side of the Moon (5)
 1- The Dark Side of the Moon (5)
```

## Output

album_ranker will complain about badly-formatted lists, e.g. one that omits/repeats a ranking number, or includes albums not part of the master set. It will also print an error message if it can't identify the album a line of input is meant to refer to, with misspellings being the most common problem.

Look for output like:
```
Could not process list for username Bad 1, failed on line 18. Vapor Trials
Bad ranking numbers for user Bad 2, remaining numbers are {15}
Bad ranking numbers for user Bad 3, remaining numbers are {15}
```

If all goes well, you'll see output that looks like:
```
Pink Floyd Studio Albums Ranked by 53 People
============================================
15. The Endless River: average rank=12.974, average star rating=--
14. Ummagumma: average rank=12.485, average star rating=--
13. More: average rank=11.499, average star rating=--
12. A Momentary Lapse of Reason: average rank=11.163, average star rating=--
11. The Final Cut: average rank=10.054, average star rating=--
10. The Division Bell: average rank=9.362, average star rating=--
9. A Saucerful of Secrets: average rank=8.849, average star rating=--
8. Atom Heart Mother: average rank=8.329, average star rating=--
7. Obscured by Clouds: average rank=8.299, average star rating=--
6. Piper at the Gates of Dawn: average rank=7.712, average star rating=--
5. The Wall: average rank=5.191, average star rating=--
4. Meddle: average rank=4.624, average star rating=--
3. Animals: average rank=3.701, average star rating=--
2. The Dark Side of the Moon: average rank=3.031, average star rating=--
1. Wish You Were Here: average rank=2.881, average star rating=--

Statistical Analysis
============================================
Most underrated Pink Floyd albums: The Endless River: 2.026, Ummagumma: 1.515, More: 1.501
Most overrated Pink Floyd albums: Wish You Were Here: -1.881, Piper at the Gates of Dawn: -1.712, Obscured by Clouds: -1.299
Most fairly-ranked Pink Floyd albums: A Saucerful of Secrets: 0.151, The Wall: 0.191, Atom Heart Mother: 0.329
Most controversial Pink Floyd albums: Piper at the Gates of Dawn: 13.937, Ummagumma: 11.594, Atom Heart Mother: 9.771
Least controversial Pink Floyd albums: Wish You Were Here: 3.192, Meddle: 3.785, The Endless River: 4.535
Most negative dissent: The Dark Side of the Moon at 2.000/3.031 (lowest median-to-mean)
Most positive dissent: Ummagumma at 14.000/12.485 (highest median-to-mean)

etc...
```

## Clusters

To print cluster info, run like so:
```commandline
$ python3 album_ranker.py --file bands/RushLists.txt --clusters 3 --top_n_slots 5
```

This will hopefully lead to output like:
```
Fans Clusters (K-Means Clustering)
============================================
Most fans best fit one of the following. Select one of these top 5 / bottom 3 lists. * = not shared across all lists.
Cluster 1 (18 fans): Moving Pictures, 2112 *, Hemispheres *, Permanent Waves, A Farewell to Kings *... Test for Echo, Roll the Bones *, Presto *
Cluster 2 (18 fans): Moving Pictures, Permanent Waves, Hemispheres *, Signals *, 2112 *... Presto *, Vapor Trails *, Test for Echo
Cluster 3 (11 fans): Moving Pictures, Signals *, Power Windows *, Grace Under Pressure *, Permanent Waves... Snakes and Arrows *, Caress of Steel *, Test for Echo
```

For the band Rush, fans break down into some obvious camps. Cluster 1 is old-school fans, who prefer the band's early prog rock sound, cluster 2 is fans of the most popular stuff, and cluster 3 is fans of Rush's 1980s synth period (like me). As a Rush fan, I knew of these three groups, but it was interesting to see the algorithm discover them on its own.

You can also use the `--random` argument:
```commandline
$ python3 album_ranker.py --file bands/PinkFloydLists.txt --clusters 3 --top_n_slots 5 --random
```

This is helpful because the K-Means algorithm in its standard form doesn't always identify distinct fan groups. Running the program repeatedly with a randomizing factor turned on can yield different results. 

## Ideas for the Future

It would be interesting to fully automate this program, to have it be able to scrape data directly from the web.

Could machine-learning come into play as well? Could I ask ChatGPT to take a fifteen line ranking list, presented in raw form with spelling mistakes and omissions (e.g. "Dark Side" instead of "Dark Side of the Moon"), and tell me the actual names of albums being referred to?