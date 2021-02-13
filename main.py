from reddit.retriever import retrieve_comment_data
from reddit.extractor import deep_extract_reply_bodies, deep_extract_replies_from_comments
from reddit.analyzer import *
from reddit.report_writer import *

import yaml
import sys

json_indicator = ".json"
request_headers = {'User-agent': 'scanner bot 0.1'}

conf_file_path = sys.argv[1]
conf_file = open(conf_file_path).read()
reddit_conf = yaml.load(conf_file, yaml.SafeLoader)["reddit"]
reddit_base_url = reddit_conf["base_url"]
reddit_subreddits = reddit_conf["subreddits"]
reddit_comment_sort = reddit_conf["comment_sort"]
reddit_buzz_keywords = reddit_conf["buzz_keywords"]
reddit_emotion_keywords = reddit_conf["emotion_keywords"]
reddit_trending_words_threshold = reddit_conf["trending_words_threshold"]
limit = reddit_conf["limit"]
num_pages_to_retrieve = reddit_conf["num_pages_to_retrieve"]

reddit_analysis_data = []
for subreddit in reddit_subreddits:
  print("Analyzing buzz for " + subreddit + "; Using limit " + str(limit))
  reddit_hot_path = subreddit + "/" + reddit_comment_sort + "/.json?limit=" + str(limit)
  comments = retrieve_comment_data(reddit_base_url, reddit_hot_path, json_indicator, request_headers, num_pages_to_retrieve)
  replies = deep_extract_replies_from_comments(comments)

  total_keyword_hits = 0
  for kw in reddit_buzz_keywords:
    total_keyword_hits += kw.get("hits", 0)

  analysis = analyze_comments_for_buzz(replies, reddit_emotion_keywords, reddit_buzz_keywords)
  reddit_buzz_keywords = analysis["keywords"]
  trending_words = analysis["trending_words"]
  reddit_analysis_data.append({
    "subreddit": subreddit,
    "query_path": reddit_hot_path,
    "limit": limit,
    "num_comments_analyzed": len(comments),
    "keywords": keyword_info(reddit_buzz_keywords),
    "total_keyword_hits": total_keyword_hits,
    "trending_words": map_trending_words(trending_words, reddit_trending_words_threshold)
  })

reddit_report = generate_report_reddit(reddit_analysis_data)
reddit_report_path = write_report([reddit_report])

print("Report written to " + reddit_report_path)


