
# def copy_subreddit(subreddit):
#     dest = {}
#     copy_attributes(dest, subreddit, subreddit_attributes)
#     return dest

def copy_submission(submission):
    # https://github.com/praw-dev/praw/blob/master/praw/models/reddit/submission.py#L550

    dest = vars(submission).copy()

    if '_reddit' in dest:
        dest.pop('_reddit', None)

    if 'author' in dest:
        dest['author'] = str(submission.author)

    if 'subreddit' in dest:
        dest['subreddit'] = str(submission.subreddit)

    if 'poll_data' in dest:
        dest['poll_data'] = str(submission.poll_data)

    return dest

def copy_comment(comment):
    # https://github.com/praw-dev/praw/blob/master/praw/models/reddit/comment.py#L174

    dest = vars(comment).copy()

    if '_reddit' in dest:
        dest.pop('_reddit', None)

    if '_submission' in dest:
        dest['_submission'] = str(comment._submission)

    if 'author' in dest:
        dest['author'] = str(comment.author)

    if '_replies' in dest:
        dest['_replies'] = str(comment._replies)

    if 'subreddit' in dest:
        dest['subreddit'] = str(comment.subreddit)

    return dest

def copy_redditor(redditor):
    # https://github.com/praw-dev/praw/blob/master/praw/models/reddit/redditor.py#L148

    dest = vars(redditor).copy()

    if 'subreddit' in dest:
        dest['subreddit'] = str(redditor.subreddit)

    return dest
