import os
import praw
import pandas as pd
from pprint import pprint

output_folder = "out"
submissions_limit=2

subreddits = [
    "MachineLearning",
    "GPT3",
    "artificial",
    "ArtificialInteligence",
    "neuralnetworks",
    "deeplearning",
    "DeepLearningPapers",
    "OpenAI",
    "datascience",
    "datamining",
    "bigdata",
    "deepmind"
]

subreddit_attributes = [
    "display_name",
    "created_utc",
    "description",
    "public_description",
    "subscribers",
    "id",
]
subreddit_trim = [
    "description",
    "public_description",
]

submission_attributes = [
    "author",
    "author_premium",
    "created_utc",
    "downs",
    "gilded",
    "score",
    "title",
    "distinguished",
    "is_original_content",
    "id",
    "name",
    "num_comments",
    "stickied",
    "upvote_ratio",
]

submission_trim = [
    "title",
]

comment_attributes = [
    "author",
    "body",
    "can_gild",
    "controversiality",
    "created_utc",
    "depth",
    "downs",
    "gilded",
    "score",
    "parent_id",
    "id",
    "distinguished",
    "is_submitter",
]

comment_trim = [
    "body",
]

redditor_attributes = [
    "comment_karma",
    "created_utc",
    "has_verified_email",
    "is_mod",
    "link_karma",
    "name",
    "total_karma",
    "verified",
]

def add_awards(data, awards):
    data["awards"] = ";".join([a["name"] for a in awards])
    data["different_awards"] = len(awards)
    c = 0
    for a in awards:
        c += awards["count"]
    data["total_awards"] = c

def add_author(data, author):
    _ = author.comment_karma
    for a in redditor_attributes:
        data["redditor_{}".format(a)] = author[a]

def extract_comments(submission, comments_data):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        data = trim_data(vars(comment), comment_trim)
        # add_awards(data, vars(comment)["all_awardings"])
        # add_author(data, vars(comment.author))
        add_data(comments_data, data)

def extract_submissions(subreddit):
    submissions = subreddit.hot(limit=submissions_limit)
    submissions_data = initialize_data(submission_attributes)
    comments_data = initialize_data(comment_attributes)
    i = 0
    for submission in submissions:
        _ = submission.title
        print("{}:{}:{}".format(subreddit.display_name, i, submission.title))
        i+=1
        add_data(submissions_data, trim_data(vars(submission), submission_trim))
        extract_comments(submission, comments_data)
    data_to_csv(submissions_data, "{}_submissions".format(subreddit.display_name))
    data_to_csv(comments_data, "{}_comments".format(subreddit.display_name))

def process_subreddit(reddit_client, subreddit_name):
    subreddit = reddit_client.subreddit(subreddit_name)
    _ = subreddit.title
    add_data(subreddit_data, trim_data(vars(subreddit), subreddit_trim))
    extract_submissions(subreddit)

def initialize_data(headers):
    data = {}
    for h in headers:
        data[h] = []
    return data

def trim_data(data, attributes):
    for a in attributes:
        data[a] = data[a].replace(",", " ").replace("\n", " ")
    return data

def add_data(data, attributes):
    for a in data:
        data[a].append(attributes[a])

def get_output_path(filename):
    return os.path.join(output_folder, filename)

def data_to_csv(data, filename):
    pd.DataFrame(data).to_csv(get_output_path("{}.csv".format(filename)), index=False)

def main():
    reddit_client = praw.Reddit("api_test", user_agent="Python:com.example.evaluationofcompetencies:v0.1 (by /u/gonzalocl1024)")
    # process_subreddit(reddit_client, subreddits[1])
    for subreddit in subreddits:
        process_subreddit(reddit_client, subreddit)

if __name__ == '__main__':
    subreddit_data = initialize_data(subreddit_attributes)
    main()
    data_to_csv(subreddit_data, "subreddit_data")
