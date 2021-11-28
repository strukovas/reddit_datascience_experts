
import argparse
import datetime
import json
import pandas as pd
import random
from pprint import pprint
import datetime

date_format = '%Y-%m-%d'

def save_csv(submissions, redditors, output_path):

    headers = [
        'id', # name, name
        'parent_id', # , parent_id

        # user
        'author', # author[name], author[name]
        'submission karma', # author[link_karma]
        'comment karma', # author[comment_karma]
        'account age', # now-author[created_utc]

        # submission
        'date', # created_utc, created_utc
        'score', # score,
        'upvote ratio', # upvote_ratio,
        'total awards received', # total_awards_received,
        'gilded', # gilded if can_gild else 'cant gild',
        'submission title', # title,
        'submission text', # selftext,

        # comment
        'time', # , created_utc-submission[created_utc]
        'score', # , score
        'total awards received', # , total_awards_received
        'gilded', # , gilded if can_gild else 'cant gild'
        'comment depth', # , depth
        'comment text' # , body
    ]

    separator_row = [
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########',
        '########'
    ]

    i = 0
    df = pd.DataFrame(columns=headers)

    time_now = datetime.datetime.now(tz=datetime.timezone.utc)

    for s in submissions:

        submission = s['submission']
        submission_author = submission['author']
        submission_time = datetime.datetime.fromtimestamp(submission['created_utc'], tz=datetime.timezone.utc)

        r = [
            submission['name'],
            '',

            submission_author,
            redditors[submission_author]['link_karma'] if submission_author in redditors else '',
            redditors[submission_author]['comment_karma'] if submission_author in redditors else '',
            time_now-datetime.datetime.fromtimestamp(redditors[submission_author]['created_utc'], tz=datetime.timezone.utc) if submission_author in redditors else '',

            submission_time.strftime(date_format),
            submission['score'],
            submission['upvote_ratio'],
            submission['total_awards_received'],
            submission['gilded'] if submission['can_gild'] else 'cant gild',
            submission['title'],
            submission['selftext'],

            '',
            '',
            '',
            '',
            '',
            ''
        ]

        df.loc[i] = r
        i += 1

        for comment in s['comments']:

            comment_author = comment['author']
            comment_time = datetime.datetime.fromtimestamp(comment['created_utc'], tz=datetime.timezone.utc)

            r = [
                comment['name'],
                comment['parent_id'],

                comment_author,
                redditors[comment_author]['link_karma'] if comment_author in redditors else '',
                redditors[comment_author]['comment_karma'] if comment_author in redditors else '',
                time_now-datetime.datetime.fromtimestamp(redditors[comment_author]['created_utc'], tz=datetime.timezone.utc) if comment_author in redditors else '',

                comment_time.strftime(date_format),
                '',
                '',
                '',
                '',
                '',
                '',

                comment_time-submission_time,
                comment['score'],
                comment['total_awards_received'],
                comment['gilded'] if comment['can_gild'] else 'cant gild',
                comment['depth'] if 'depth' in comment else '',
                comment['body'] if 'body' in comment else ''
            ]

            df.loc[i] = r
            i += 1

        df.loc[i] = separator_row
        i += 1

    df.to_csv(output_path, index=False)

def submissions_by_month_randomized(submissions, seed):

    submissions_by_month = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: []
    }

    for submission in submissions:

        date = datetime.datetime.fromtimestamp(submission['submission']['created_utc'])
        submissions_by_month[date.month].append(submission)

    rand = random.Random(seed)

    for month in submissions_by_month.values():
        rand.shuffle(month)

    return submissions_by_month

def select_submissions(submissions_by_month, max_total_comments, seed):

    total_submissions = 0

    for month in submissions_by_month.values():
        total_submissions += len(month)

    proportions = {}

    for month, submissions in submissions_by_month.items():
        proportions[month] = len(submissions)/total_submissions

    selected = []
    selected_count = 0
    rand = random.Random(seed)

    # TODO check no infinite loop
    # TODO if max_total_comments is None
    while True:

        for month, submissions in submissions_by_month.items():

            r = rand.random()

            if len(submissions) > 0 and r < proportions[month]:

                s = submissions.pop()
                selected.append(s)
                selected_count += len(s['comments'])

                if selected_count >= max_total_comments:
                    return selected

def redditors_by_name(redditors_by_fullname):

    redditors = {}

    for redditor in redditors_by_fullname.values():
        redditors[redditor['name']] = redditor

    return redditors

# def ups_downs_score(o):
#     if o['downs'] != 0 or o['ups'] != o['score'] or o['gilded'] != 0:
#         # downs are always 0, ups and score are always equal, gilded changes
#         print(o['name'], o['score'], o['ups'], o['downs'], o['gilded'])
#     if o['banned_by'] is not None:
#         # is always None
#         print(o['name'], o['score'], o['ups'], o['downs'], o['gilded'], o['banned_by'])
#     if o['clicked'] is not None:
#         print(o['name'], o['score'], o['ups'], o['downs'], o['gilded'], o['clicked'])

def find_submissions_in_range(submissions, min_comments, max_comments):

    if min_comments is None:
        min_comments = 0

    if max_comments is None:
        return list(filter(lambda s: min_comments <= len(s['comments']), submissions))

    return list(filter(lambda s: min_comments <= len(s['comments']) <= max_comments, submissions))

def get_excluded_ids(exclude_ids):

    if exclude_ids is None:
        return set()

    excluded_ids = set()

    for csv_path in exclude_ids:
        ids = pd.read_csv(csv_path)['id']
        excluded_ids.update(list(ids))

    return excluded_ids

def remove_excluded(submissions, excluded_ids):

    included_submissions = []

    for submission in submissions:

        if submission['submission']['name'] in excluded_ids:
            continue

        included_comments = []

        for comment in submission['comments']:

            if not comment['name'] in excluded_ids:
                included_comments.append(comment)

        included_submissions.append({'submission': submission['submission'], 'comments': included_comments})

    return included_submissions

def remove_max_depth(submissions, max_depth):

    if max_depth is None:
        return submissions

    max_depth_submissions = []

    for submission in submissions:

        max_depth_comment = []

        for comment in submission['comments']:

            if comment['depth'] <= max_depth:
                max_depth_comment.append(comment)

        max_depth_submissions.append({'submission': submission['submission'], 'comments': max_depth_comment})

    return max_depth_submissions

def main(input_path, redditors_path, output_path, min_comments, max_comments, max_total_comments, seed, max_depth,
         exclude_ids):

    with open(input_path) as input_file:
        submissions = json.load(input_file)

    # for submission in submissions['submissions']:
    #     ups_downs_score(submission['submission'])
    #     for comment in submission['comments']:
    #         ups_downs_score(comment)

    with open(redditors_path) as input_file:
        redditors = json.load(input_file)

    excluded_ids = get_excluded_ids(exclude_ids)

    redditors = redditors_by_name(redditors['redditors'])

    submissions = submissions['submissions']
    submissions = remove_excluded(submissions, excluded_ids)
    submissions = remove_max_depth(submissions, max_depth)
    submissions = find_submissions_in_range(submissions, min_comments, max_comments)
    submissions = submissions_by_month_randomized(submissions, seed)
    submissions = select_submissions(submissions, max_total_comments, seed)

    save_csv(submissions, redditors, output_path)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str)
    parser.add_argument('redditors_path', type=str)
    parser.add_argument('output_path', type=str)
    parser.add_argument('--min_comments', type=int)
    parser.add_argument('--max_comments', type=int)
    parser.add_argument('--max_total_comments', type=int)
    parser.add_argument('--seed', default=1024, type=int)
    parser.add_argument('--max_depth', type=int)
    parser.add_argument('--exclude_ids', type=str, nargs='*', help='list of csv files with at least one column id')
    args = parser.parse_args()

    main(args.input_path,
         args.redditors_path,
         args.output_path,
         args.min_comments,
         args.max_comments,
         args.max_total_comments,
         args.seed,
         args.max_depth,
         args.exclude_ids)
