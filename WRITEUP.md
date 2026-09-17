# HW0 writeup

**Name:** Kaif Kassam
**Date:** 2026-09-16

Replace every placeholder below with your answer. Every number you give comes from a script in this repo; say which one.

## Part 1. Basic rating statistics

Code: `human_part1.py`. One or two sentences per answer, with the numbers.

**(a) How many ratings, users, and movies are there, and how are ratings distributed across 1–5 stars?**
 
 Total number of ratings is 100,000, total number of users is 943, and total number of movies is 1682. This is how the ratings are distributed:

Ratings by star groups: rating
1     6110
2    11370
3    27145
4    34174
5    21201


**(b) What is the median number of ratings per user, and how many users have 100 or more ratings?**

The median number of ratings per user is 65. 364 users have 100+ ratings.

**(c) Which 10 movies have the most ratings?**

These 10 movies have the most number of ratings:

Star Wars (1977)                 583
Contact (1997)                   509
Fargo (1996)                     508
Return of the Jedi (1983)        507
Liar Liar (1997)                 485
English Patient, The (1996)      481
Scream (1996)                    478
Toy Story (1995)                 452
Air Force One (1997)             431
Independence Day (ID4) (1996)    429


**(d) Among movies with at least 20 ratings, which 10 have the highest mean rating?**

The following (out of movies with 20 or more ratings) have the highest mean rating:

Close Shave, A (1995)
Schindler's List (1993)
Wrong Trousers, The (1993)
Casablanca (1942)                                 
Wallace & Gromit: The Best of Aardman Animation...
Shawshank Redemption, The (1994)
Rear Window (1954) 
Usual Suspects, The (1995)
Star Wars (1977)
12 Angry Men (1957)

**Anything you got stuck on (what you tried, where it broke), or "none":**

It's been a minute since I've done any python, took quite some searching to figure out how to get this running. But I remember how intuitive the syntax is and it's kind of coming back now.

## Part 2. The best movie

Code: `human_part2.py`.

**My rule:** "A stood the test of time" rating - essentially weighting the impact of an indvidual rating of a movie on the average by the difference between the release date and timestamp of that individual rating.

**One rule I considered and rejected, and why:** I thought of using the gender or zip_code data to build a top 10 out of that - see the top 10 out of the most concentrated zipcodes. That does not answer the same questions as what is the Top 10 from above and I don't think concentration of reviews in a particular zipcode translates to them being the better reviewers/reviews to account.

**Top 10 under my rule:**

These are the top 10 under my rule:

Schindler's List (1993)
Star Wars (1977)
Shawshank Redemption, The (1994)
Casablanca (1942)
Usual Suspects, The (1995)
Godfather, The (1972)
Rear Window (1954)
Silence of the Lambs, The (1991)
Raiders of the Lost Ark (1981)
One Flew Over the Cuckoo's Nest (1975)


**Why my rule, in at most 150 words. Name one thing it gains and one thing it loses:**

The goal of my rule is to account for movies with fewer ratings that incorrectly be indicating well-favored movies while also adding an element that looks into how connected users are to a movie over that and quantifying that in the final mean calculation. The gain is in identifying a stronger pattern of "really good" movies that have been reviewed strongly over a stretch of time. The obvious loss is that some movies just have not had been out there that long, which one probably requiring a weight of its own somehow (this was already getting quite complicated, I"ll leave that one for another day).

## Part 3. The most ___ movie

Code: `human_part3.py`.

**My adjective:** "Artsy"

**My definition** (one sentence, precise enough that a classmate could code it)**:** The kind of movies that people with occupations related to the arts (specifically writers, artists, and people in entertainment) are inclined to like, empiraclly speaking.

**One definition I considered and rejected, and why:**

I was considering looking into movies enjoyed by people falling under the retired category. I ended up deciding it was too broad a category (unaware of the individual backgrounds of the individuals) to use to make claims.


**Top 5 under my definition:**

The top 5 under my definition are the following:

Rosencrantz and Guildenstern Are Dead (1990)
Wrong Trousers, The (1993
Psycho (1960)
Jean de Florette (1986)
Chinatown (1974)

**What your definition captures, what it misses, and where "___-ness" lives in this data — the
genre labels, what the crowd did, or the words in the titles. At most 150 words:**

The "artsy-ness" lives in the occupation data of the users. The movies seem to be more old classics with wide genres rather than a pool of movies with similar characteristics that may indicate a relation to "artsy" occupations. None overlap with the crowd's top 10 list. Th data shows us that people in "artsy" occupation value different films compared to the broader group averaged out (althought we have not averaged out a group without the arts occupations).

## Part 4. Claude's answers

Claude answers the same three questions in `claude_answers_1_2_3.py`, without seeing your code
or your answers.

**Did its numbers for Part 1 match yours? If not, which, and what did you find?**

All of them matched my numbers.

## Part 5. Comparing the best movie

**Claude's rule:**

Claude rule was as found below:

"Best" can't just mean "highest average rating": with only 20 ratings required to
qualify, a handful of enthusiastic fans can push an obscure movie to a perfect
5.0 average. The fix is the same one IMDb uses for its Top 250: shrink each
movie's mean toward the dataset-wide average, by an amount that depends on how
few ratings it has. A movie with 3 ratings gets pulled almost all the way back
to the global mean; a movie with 500 ratings barely moves. This is a Bayesian
average (posterior mean with a Beta/Normal-ish prior):

**Read what Claude wrote about its rule. Does it anywhere admit the rule was a choice, and that a different rule was possible? Or does it give its answer as simply the answer? Quote the sentence that decides it:**

Claude is very set on how IMDB calculates its top 250 list. There is no acknolwedgement of other potential routes to this question. 

"The fix is the same one IMDb uses for its Top 250: shrink each movie's mean toward the dataset-wide average, by an amount that depends on how few ratings it has." 

"The Fix" clearly shows us that the model has decided right away that this is how it and we should go about this problem.

**Your Part 2 top 10 and Claude's Part 2 top 10 — not the Part 1(d) lists. Where do they differ, and why?**

I searched up how IMDB does its ratings before I started this. It just made most sense to me to look into the ratings platform that I use the most. That's why most of our list looks similar - with some movies being in different positions because of the additional waiting by time difference that I've added to my rule. I also use a much higher constant which might explain why 4 movies are not shared across the two lists.

**Better for what purpose? Name a situation where your rule is the right one and a situation where Claude's is. At most 150 words. You may conclude yours, its, or neither:**

I'm still biased towards IMDBs approach since that's what I've always used as a reference and its just IMDB so I'm assuming they a strong basis for using this approach (I'm limiting myself to one outlook here like claude, maybe). I do think my rule in some way may be a more robust way to determine an "all time" top 10 to top 20 list - but I'm not too sure.

## Part 6. Comparing the most ___ movie

**Claude's definition:**

This is Claude's definition:

"Artsy" is a genre-flavor question, not a rating-quality question, so I built a
genre score instead of looking at stars. I hand-labeled each of the 19 genres as
art-house-coded, mainstream/commercial-coded, or neutral, based on the kind of
movie that genre usually signals.

Claude looks into the genres weights and sums them to determine an artsiness score. 

**Is Claude's film in your top 5?**

It is not in my top 5. Interestingly both of "us" picked an arts related approach - I took on occupation as a way to determine the most "artsy" movies and Claude defined weights by genres that it labelled -we do not share any common names in the top 5 list.

**What Claude's definition sees that yours does not, and the reverse. At most 150 words:**

Claude's definition is focused on the movies themselves and what genres they would be categorized as. My approach looks at who has rated these movies. Mine does assume people in more art related fields of work would be more likely to watch "artsy" cinema - which is a gap the gnere approach fills.

## Working with Claude

**What you asked Claude for during Parts 1–3** (debugging and installing only — say what you
got stuck on)**:**

 Mainly for the installation part and get past some issue with the uv set up. I then used it for extracting information from my terminal responses and figuring out where I was getting stuck with python syntax.

**Something Claude said that you could not verify, and why. Or "none," and how you checked:**

none

**What you would do differently next time, in 3–5 sentences:**

I would read through all the parts multiple times before I start the process. I did find myself somewhat overwhelmed by the fact that I had to contiuously refer back to minor details. I rather have a clear understanding and possibly write it down in my notebook before I take on the next hw.

**Where did this assignment slow you down for a reason that was its fault, not yours? Point at
the step. Or "nowhere." One or two sentences:**

Nowhere

**Hours spent:** 6 hours

**Anyone who helped you, or "no one":** 

Friend, mac Alum now software engineer and big movie nerd. Great that we were hanging out, used quite some of his help - always helps to have someone to talk through these questions with.
