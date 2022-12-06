import praw
import spacy
import csv
from tqdm import tqdm

# Ideally this is in some sort of settings file
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='ct experiment')

# testing these two just for validities sake
list_of_CT_subreddits = ['programming', 'learnprogramming', 'cscareerquestions', 'ProgrammerHumor', 'ProgrammerTIL',
                         'AskProgramming', 'coding', 'compsci', 'dailyprogrammer', 'netsec', 'webdev', 'gamedev', 'cscareerquetions',
                         'javascript', 'python', 'java', 'cpp', 'csharp', 'golang', 'rust', 'php', 'c_programming', 'sql', 'swift',
                         'typescript', 'ruby', 'haskell', 'rstats', 'kotlin', 'matlab', 'scala', 'latex', 'lisp', 'dartlang', 'clojure',
                         'elixir', 'julia', 'perl', 'asm', 'lua', 'elm']
csv_field_names = ["explanation_text", "author", "is_author_ct",
                   "explanation_sentence_count", "explanation_word_count", "explanation_nesting_level_count", "explanation_score", "parent_submission_id"]

subreddit = reddit.subreddit('howto')
nlp = spacy.load('en_core_web_md')


def get_subreddit_name_from_comment(comment):
    return comment.subreddit.display_name

# Template


def calculate_comment_score(comment):
    return comment.score


def has_intersection(a, b):
    return True if list(set(a) & set(b)) else False

# This should just return the list of comments


def get_top_level_comments(submission):
    return submission.comments[0:5]


def get_submissions():
    return subreddit.search("flair:Solved", limit=5000)


def is_author_ct(author):
    # create a list of first 100 subreddit names that author has submitted to recently
    author_subreddits = list(
        map(get_subreddit_name_from_comment, author.comments.new(limit=200)))

    # if the author subreddits intersect with the list of ct subreddits at all, the author is ct
    return has_intersection(author_subreddits, list_of_CT_subreddits)

#


def create_explanation_dict(comment):
    try:
        data = {
            "explanation_text": comment.body,
            "author": comment.author.name,
            "is_author_ct": is_author_ct(comment.author),
            "explanation_sentence_count": calculate_comment_steps(comment),
            "explanation_word_count": calculate_word_count(comment),
            "explanation_nesting_level_count": calculate_nesting_text(comment),
            "explanation_score": calculate_comment_score(comment),
            "parent_submission_id": comment.submission.id
        }
    except:
        data = {
            "explanation_text": "error",
            "author": "error",
            "is_author_ct": False,
            "explanation_sentence_count": 0,
            "explanation_word_count": 0,
            "explanation_nesting_level_count": 0,
            "explanation_score": 0,
            "parent_submission_id": "error"
        }
    print(data)
    return data

# set delimeter as | because commas are common in text


def write_dicts_to_csv(dicts, file_name, field_names):
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(dicts)

# my custom delimeter stuff might not work. Might just have to go off word count and sentences


def calculate_comment_steps(comment):
    doc = nlp(comment.body)
    # separate based on commas too
    re_tokenized = [str(sub).split(',') for sub in doc.sents]
    # flatten the resulting list
    re_tokenized = [item for sublist in re_tokenized for item in sublist]
    return (len(list(re_tokenized)))


def calculate_word_count(comment):
    doc = nlp(comment.body)
    words = [token.text for token in doc]
    return len(words)

# tokenizes into paragraphs


def tokenize_paragraphs(document):
    start = 0
    for token in document:
        if token.is_space and token.text.count("\n") > 1:
            yield document[start:token.i]
            start = token.i
    yield document[start:]

# counts the number of paragraphs


def count_paragraphs(comment):
    return len(list(tokenize_paragraphs(nlp(comment.body))))

# we can only count 2 levels in raw text so we return 2 or 1


def calculate_nesting_text(comment):
    return 2 if count_paragraphs(comment) > 1 else 1


if __name__ == "__main__":

    submissions = get_submissions()
    analyses = []

    for submission in submissions:
        comments = get_top_level_comments(submission)
        analyses = analyses + list(map(create_explanation_dict, comments))

    print(analyses)
    # print("num analyses:" + str(len(analyses)))

    write_dicts_to_csv(analyses, "solved.csv", csv_field_names)
