
from psaw import PushshiftAPI

import datetime
import logging
import json
import os

pushshift_client = PushshiftAPI()

def submission_ids(subreddit, time_after, time_before):
    submissions = pushshift_client.search_submissions(subreddit=subreddit,
                                                      after=time_after,
                                                      before=time_before)
    return [submission.id for submission in submissions]

def get_output_path(output_folder, name):
    return os.path.join(output_folder, "ids_{}.json".format(name))

def enable_logger():
    handler = logging.FileHandler(filename='out/psaw.log')
    handler.setLevel(logging.INFO)

    logger = logging.getLogger("psaw")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def main():

    enable_logger()

    subreddits = [
        # "MachineLearning",
        # "GPT3",
        # "artificial",
        # "ArtificialInteligence",
        # "neuralnetworks",
        # "deeplearning",
        # "DeepLearningPapers",
        # "OpenAI",
        "datascience",
        # "datamining",
        # "bigdata",
        # "deepmind"
    ]
    output_folder = "out"

    time_after = int(datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc).timestamp())
    time_before = int(datetime.datetime(2020, 12, 31, tzinfo=datetime.timezone.utc).timestamp())
    time_save = int(datetime.datetime.now().timestamp())

    os.makedirs(output_folder, exist_ok=True)

    all_ids = {}

    for subreddit in subreddits:
        ids = submission_ids(subreddit, time_after, time_before)

        all_ids[subreddit] = ids

        save_ids = {
            "subreddit": subreddit,
            "time_after": time_after,
            "time_before": time_before,
            "time_save": time_save,
            "submission_ids": ids
        }

        output_path = get_output_path(output_folder, subreddit)

        with open(output_path, "w") as output_file:
            json.dump(save_ids, output_file)

    save_ids = {
        "time_after": time_after,
        "time_before": time_before,
        "time_save": time_save,
        "submission_ids": all_ids
    }

    output_path = os.path.join(output_folder, "submission_ids.json")

    with open(output_path, "w") as output_file:
        json.dump(save_ids, output_file)

if __name__ == "__main__":
    main()
