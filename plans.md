# Just brainstorming

## Next Steps

### Tuesday, November 1st, 2022

* got reasonable output to csv and the thing scales up to handle more comments now
* got basic NLP counts going

* Next major priority:
    * create the list of CT stuff
    * run a test ... probably going to need to put this on a server to run over night
    * set it for like 100 submissions and just let it go

* Nice to have: 
    * lots of hardcoded values need to be extracted and put into a settings file or something
* Nice to have:
    * dealing with lists and bullet points

### Monday, October 31st, 2022

* Got is_author_ct working and some of the initial structure
* need to break up the get_top_level_comments function to be more modular - it's currently acting like main
* calculate granularity is a next week task honestly
* so really we just need to test this sucker at scale now
    * we also need to define some sort of output format
    * So that's the pandas type stuff

* I could probably just do this later tonight. If I can get going on this software early it frees up 
  so much of my time and schedule. Might be smart to just slam back a redbull and fucking murder this project
* need to make the code more flexible for the number of comments and submissions

## some shit from before
* so what do you have so far?
* I can scrape a bunch of reddit posts
* I can get data about a user and some of their comments


* let's get their affiliations/subreddits
  * going to need to generate a list of techy subreddits
    * r/programming r/technology probably tech probably too generic
  * Could get affiliations by getting the subreddits that they post to
    * submission.wherethefucksithisposted?



Things I'll need to consider
* rate limits
* how do I store this data effectively?
  * is it really just big ass text files?
  * probably json
  * probably can't store this data on firebase or something

Review what you did
* Just chaotically explored PRAW and other options for scraping reddit data
* great progress to familiarize myself with API and selecting platforms

What to work on next time
* want to read through the APIs a little more carefully
* maybe find a youtube tutorial or some example repositories
* NLP portion needs to be explored


## Pipeline

* Reddit:
    * scrape many submissions with the flairs solved or SeriousAnswersOnly
    * Scrape the top 10 TOP LEVEL comments (more or less)
    * Gather the commenter's most recent X posts:
        * get the subreddits those posts are from
        * check if any of those subreddits are in a list of coding related subreddits
        * if so - flag user as CT or flag comment itself as CT
    * Store the comment text + CT flag

    * repeat for N entries where N is enough to get reasonable amounts of data



* NLP:
    * loop through each comment
    * assess level of granularity:
        * sentence count
        * paragraph count
        * May need to do some custom tokenization (based on "and" as well as ",")
            * this will be added to the regular sentence tokenizing process
            * could just nest this
    * Store estimated # of steps in spread sheet

* Doing additional delimeters
    * I have sentences
    * loop through each sentence
    * break it using python's not shit tier string management
    * sum


* what's my question here? Dealing with a diverse set of styles of text
* Reddit comments are markdown!
* some sort of markdown analysis could actually be really useful
* can search for paragraphs, numbered or bulleted
* Numbered and bulleted lists can gather their level of nesting
    * I'm asking how do we store values about nesting steps?
    * how do things like numbered lists work?
* Going to have to devise some better methods for this
    * check for the presence of bullet points or numbers
    * if present do analysis based on markdown
    * if not present - do standard NLP


## Data Storage

* Json vs csv
* Going with CSV - we'll flatten some of the data

### Converting highly nested data

* Total # of levels
    * if no bullets/numbered lists - paragraphs and sentences
    * if bullets/numbered lists - use markdown to analyze nesting
* Total # of steps
    * if no bullets/numbered lists - sentence + and + ,
    * if bullets/numbered lists - count the # of elements

### CSV structure

* text
* is_CT
* # of levels
* # of steps
* formatting - list vs paragraph
    * provides insight into thinking

### Json vs CSV

JSON
* greater flexibility in the types and structure of data we store
* deeper analysis can be performed
* additional analysis and still probalby have to put this into a CSV at the end of the day

CSV
* CSV easier to analyze
* quicker, fewer steps
* more assumptions and estimation

## Open Questions

* How do we get the markdown content of comments?
    * how do we analyze it effectively?
    * convert markdown to json representation of the AST - traverse that looking for elements
        * going to need to identify the names of different markdown elements to find all bulleted elemets
        * How does this fit into a general process?
    * quick analysis - is bullet is number present in text? If yes - markdown analysis, if no nlp analysis

* how do we store the data?
    * export to csv using what's that datascience package?
    * Also pandas:
        * Dataframe to csv
        * Create a dataframe as you go
        * convert to csv
        * Just change the delimeter of this file to '|' who the fuck types with pipes
    * there's a csv package in python
        * problem text is going to contain commas
        * dict to csv
        * can change delimeter of the file to something like '|'
        * this is a point towards JSON

