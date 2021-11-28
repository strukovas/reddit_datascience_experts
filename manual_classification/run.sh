
python generate_csv.py \
  ../subreddit_selection/out/submission_datascience_all.json \
  ../subreddit_selection/out/redditors.json \
  out/submissions.csv \
  --max_total_comments 1000 \
  --max_depth 0 \
  --exclude_ids in/*


python generate_csv.py \
  test.json \
  ../subreddit_selection/out/redditors.json \
  out/submissions.csv \
  --max_total_comments 20 \
  --max_depth 0 \
  --exclude_ids in/*

rm out/submissions.csv
python generate_csv.py \
  ../subreddit_selection/out/submission_datascience_all.json \
  ../subreddit_selection/out/redditors.json \
  out/01_submissions.csv \
  --min_comments 1 \
  --max_total_comments 20 \
  --max_depth 0 \
  --exclude_ids in/*

python generate_csv.py \
  ../subreddit_selection/out/submission_datascience_all.json \
  ../subreddit_selection/out/redditors.json \
  out/02_submissions.csv \
  --min_comments 1 \
  --max_total_comments 20 \
  --max_depth 0 \
  --exclude_ids in/*

python generate_csv.py \
  ../subreddit_selection/out/submission_datascience_all.json \
  ../subreddit_selection/out/redditors.json \
  out/03_submissions.csv \
  --min_comments 1 \
  --max_total_comments 20 \
  --max_depth 0 \
  --exclude_ids in/*

cp out/03_submissions.csv in/

python generate_csv.py \
  ../subreddit_selection/out/submission_datascience_all.json \
  ../subreddit_selection/out/redditors.json \
  out/04_submissions.csv \
  --min_comments 1 \
  --max_total_comments 20 \
  --max_depth 0 \
  --exclude_ids in/*


python generate_csv.py \
  ../subreddit_selection/out/submission_datascience_all.json \
  ../subreddit_selection/out/redditors.json \
  out/05_submissions.csv \
  --min_comments 1 \
  --max_total_comments 20 \
  --max_depth 0 \
  --exclude_ids in/*

python generate_csv.py \
  ../subreddit_selection/out/submission_datascience_all.json \
  ../subreddit_selection/out/redditors.json \
  out/06_submissions.csv \
  --min_comments 1 \
  --max_total_comments 20 \
  --max_depth 0 \
  --exclude_ids in/*

python generate_csv_submissions_ids.py \
  ../subreddit_selection/out/submission_datascience_all.json \
  ../subreddit_selection/out/redditors.json \
  out/10_submissions.csv \
  out/01_submissions.csv \
  out/02_submissions.csv \
  out/03_submissions.csv \
  out/04_submissions.csv \
  out/05_submissions.csv \
  out/06_submissions.csv \
  --max_depth 0



