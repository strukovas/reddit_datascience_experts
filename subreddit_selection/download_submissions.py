from attributes import copy_submission
from attributes import copy_comment

import praw
import json
import os
import datetime
import logging

def process_comments(submission):

    i = 0
    print("Comments: {:<6}/{:<6}".format(i, submission.num_comments), end="", flush=True)

    comments_data = []
    submission.comments.replace_more(limit=None)

    for comment in submission.comments.list():

        comment_data = copy_comment(comment)

        comments_data.append(comment_data)

        i += 1
        print("\b\b\b\b\b\b\b\b\b\b\b\b\b{:<6}/{:<6}".format(i, submission.num_comments), end="", flush=True)

    return comments_data

def process_submission(submission):

    _ = submission.title

    submission_data = copy_submission(submission)

    comments_data = process_comments(submission)

    return {
        "submission": submission_data,
        "comments": comments_data
    }

def process_submissions(reddit_client, subreddit, submission_ids, output_folder, checkpoint_interval):

    subreddit_data = {
        "subreddit": subreddit,
        "submissions": []
    }

    full_names = ["t3_{}".format(submission_id) for submission_id in submission_ids]

    i = 0
    total_ids = len(submission_ids)
    print("\r{}: {:<6}/{:<6} ".format(subreddit, i, total_ids), end="")

    for submission in reddit_client.info(fullnames=full_names):
        submission_copy = process_submission(submission)
        subreddit_data["submissions"].append(submission_copy)

        i += 1
        print("\r{}: {:<6}/{:<6} ".format(subreddit, i, total_ids), end="")

        if (i % checkpoint_interval) == 0:
            save_data(subreddit_data, output_folder, 'checkpoint_{}'.format(i))

    print()
    return subreddit_data

def get_output_path(output_folder, name, part):
    return os.path.join(output_folder, 'submission_{}_{}.json'.format(name, part))

def save_data(subreddit_data, output_folder, part):

    output_path = get_output_path(output_folder, subreddit_data['subreddit'], part)

    with open(output_path, "w") as output_file:
        json.dump(subreddit_data, output_file)

def enable_logger(log_file_path):
    handler = logging.FileHandler(filename=log_file_path)
    handler.setLevel(logging.DEBUG)
    for logger_name in ('praw', 'prawcore'):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

def main():

    input_path = 'out/submission_ids.json'
    output_folder = 'out'
    log_file_path = os.path.join(output_folder, 'praw_submissions.log')
    checkpoint_interval = 100

    enable_logger(log_file_path)

    reddit_client = praw.Reddit("api_test", user_agent="python:com.example.evaluationofcompetencies:v1.0 (by /u/gonzalocl1024)")

    with open(input_path) as input_file:
        submission_ids = json.load(input_file)

    time_after = submission_ids["time_after"]
    time_before = submission_ids["time_before"]
    time_save_ids = submission_ids["time_save"]
    time_download = int(datetime.datetime.now().timestamp())

    for subreddit in submission_ids["submission_ids"]:

        subreddit_data = process_submissions(reddit_client,
                                             subreddit,
                                             submission_ids['submission_ids'][subreddit],
                                             output_folder,
                                             checkpoint_interval)

        subreddit_data["time_after"] = time_after
        subreddit_data["time_before"] = time_before
        subreddit_data["time_save_ids"] = time_save_ids
        subreddit_data["time_download"] = time_download

        save_data(subreddit_data, output_folder, 'all')

if __name__ == '__main__':
    main()
