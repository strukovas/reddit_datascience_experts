
import praw
from pprint import pprint

def main():
    subreddit = "GPT3"
    reddit_client = praw.Reddit("api_test", user_agent="Linux:com.example.evaluationofcompetencies:v0.1 (by /u/gonzalocl1024)")
    process_subreddit(reddit_client, subreddit)

def process_subreddit(reddit_client, subreddit_name):

    subreddit = reddit_client.subreddit(subreddit_name)
    _ = subreddit.title
    print_md("subreddit", vars(subreddit))

    submission = next(subreddit.hot(limit=1))
    _ = submission.title
    print_md("submission", vars(submission))
    # print_md("award", {})
    # pprint(vars(submission)["all_awardings"])
    # print(";".join([a["name"] for a in vars(submission)["all_awardings"]]))
    # print(len(vars(submission)["all_awardings"]))
    # for a in vars(submission)["all_awardings"]:
    #     print(a["name"])

    comment = submission.comments.list()[0]
    _ = comment.author
    print_md("comment", comment)
    # print_md("flair", comment)
    # pprint(vars(comment)["all_awardings"])
    # for a in vars(comment)["all_awardings"]:
    #     print(a["name"])

    redditor = comment.author
    _ = redditor.comment_karma
    print_md("redditor", redditor)

def print_md(title, attributes):
    print("## {}\n".format(title))
    for a in attributes:
        print("* `{}`: `{}`  \n  ".format(a, attributes[a]))

if __name__ == '__main__':
    main()

# TODO flair, award, traffic, confidence