
import argparse
import json
import pandas as pd

from generate_csv import save_csv, redditors_by_name, remove_max_depth

def get_included_ids(include_ids):

    included_ids = set()

    for csv_path in include_ids:
        ids = pd.read_csv(csv_path)['id']
        included_ids.update(list(ids))

    return included_ids

def remove_excluded(submissions, included_ids):

    included_submissions = []

    for submission in submissions:

        if not submission['submission']['name'] in included_ids:
            continue

        included_comments = []

        for comment in submission['comments']:

            if comment['name'] in included_ids:
                included_comments.append(comment)

        included_submissions.append({'submission': submission['submission'], 'comments': included_comments})

    return included_submissions

def main(input_path, redditors_path, output_path, include_ids, max_depth):

    with open(input_path) as input_file:
        submissions = json.load(input_file)

    with open(redditors_path) as input_file:
        redditors = json.load(input_file)

    included_ids = get_included_ids(include_ids)

    redditors = redditors_by_name(redditors['redditors'])

    submissions = submissions['submissions']
    submissions = remove_excluded(submissions, included_ids)
    submissions = remove_max_depth(submissions, max_depth)

    save_csv(submissions, redditors, output_path)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str)
    parser.add_argument('redditors_path', type=str)
    parser.add_argument('output_path', type=str)
    parser.add_argument('include_ids', type=str, nargs='+', help='list of csv files with at least one column id')
    parser.add_argument('--max_depth', type=int)
    args = parser.parse_args()

    main(args.input_path,
         args.redditors_path,
         args.output_path,
         args.include_ids,
         args.max_depth)
