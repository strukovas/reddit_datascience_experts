
import json
import praw
import argparse
import datetime
import logging

from attributes import copy_redditor

def load_data(input_path):

    with open(input_path) as data_file:
        return json.load(data_file)

def get_redditor_names(submissions):

    author_fullname = set()

    for submission in submissions:

        if 'author_fullname' in submission['submission']:
            author_fullname.add(submission['submission']['author_fullname'])

        for comment in submission['comments']:

            if 'author_fullname' in comment:
                author_fullname.add(comment['author_fullname'])

    return author_fullname

def download_redditors(reddit_client, redditor_names):

    redditors = {}
    i = 0
    total_redditors = len(redditor_names)

    for redditor in reddit_client.redditors.partial_redditors(redditor_names):

        redditors[redditor.fullname] = copy_redditor(redditor)

        i += 1
        print('\rRedditors: {:<6}/{:<6}'.format(i, total_redditors), end='')

    print()

    return redditors

def enable_logger(log_file_path):
    handler = logging.FileHandler(filename=log_file_path)
    handler.setLevel(logging.DEBUG)
    for logger_name in ('praw', 'prawcore'):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

def main(input_path, output_path):

    enable_logger('out/praw_redditors.log')

    reddit_client = praw.Reddit('api_test', user_agent='python:com.example.evaluationofcompetencies:v1.0 (by /u/gonzalocl1024)')

    data = load_data(input_path)

    redditor_names = get_redditor_names(data['submissions'])

    redditors = {
        'time_download': int(datetime.datetime.now().timestamp()),
        'redditors': download_redditors(reddit_client, redditor_names)
    }

    with open(output_path, 'w') as redditors_file:
        json.dump(redditors, redditors_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    parser.add_argument('--output', type=str, default='out/redditors.json')
    args = parser.parse_args()
    main(args.input, args.output)
