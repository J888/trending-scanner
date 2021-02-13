# trending-scanner
Scans data sources to find trends

# Run main script

```bash
pipenv run python main.py config/config.yml
```


# Config
config.yml example

```yml
---
  reddit:
    base_url: https://www.reddit.com
    limit: 1
    num_pages_to_retrieve: 1
    subreddits:
      - /r/somesubreddit
      - /r/anothersubreddit
    comment_sort: hot
    trending_words_threshold: 20 # word has to have this many hits to be considered trending
    buzz_keywords:
      - main_term: something
        alternates: 
          - something_another_term_for_it
    emotion_keywords:
      happy: 
        - happy words

      fear:
        - fearful words

      sad:
        - some words that are sad

      angry:
        - anger indication words
        
      surprise:
        - words that indicate surprise
```
