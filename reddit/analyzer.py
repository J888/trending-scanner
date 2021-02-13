from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
import yaml

# a method to pick out the emotions in a text
# returns { 'Happy': 0, 'Sad': 0, etc. }
def analyze_emotions(text, emotion_keywords):
    happy_keywords = emotion_keywords["happy"]
    sad_keywords = emotion_keywords["sad"]
    angry_keywords = emotion_keywords["angry"]
    fear_keywords = emotion_keywords["fear"]
    surprise_keywords = emotion_keywords["surprise"]

    happy_count = 0
    sad_count = 0
    angry_count = 0
    fear_count = 0
    surprise_count = 0

    for kw in happy_keywords:
        if kw.lower() in text.lower():
            happy_count += 1

    for kw in sad_keywords:
        if kw.lower() in text.lower():
            sad_count += 1

    for kw in angry_keywords:
        if kw.lower() in text.lower():
            angry_count += 1

    for kw in fear_keywords:
        if kw.lower() in text.lower():
            fear_count += 1
    
    for kw in surprise_keywords:
        if kw.lower() in text.lower():
            surprise_count += 1

    total_emotional_words = float(happy_count + sad_count + angry_count + fear_count + surprise_count)
    if total_emotional_words == 0.0:
        return {
            "Happy": 0,
            "Sad": 0,
            "Angry": 0,
            "Fear": 0,
            "Surprise": 0
        }

    return {
        "Happy": happy_count / total_emotional_words,
        "Sad": sad_count / total_emotional_words,
        "Angry": angry_count / total_emotional_words,
        "Fear": fear_count / total_emotional_words,
        "Surprise": surprise_count / total_emotional_words
    }

def prevailing_emotion(text, emotion_keywords):
    emotion = analyze_emotions(text, emotion_keywords)
    greatest_key= ""
    greatest_value_value = -1.0
    for key in emotion:
        if emotion[key] > greatest_value_value:
            greatest_value_value = emotion[key]
            greatest_key = key
    return greatest_key

def analyze_comments_for_buzz(comments, emotion_keywords, keywords):
    trending_keywords = {}
    print("Analyzing comments for buzz", end = "", flush = True)

    for comment in comments:
        print(".", end = "", flush = True)
        
        comment_prevailing_emotion = prevailing_emotion(comment, emotion_keywords)

        words_after_filter = filter_common_words_from_sentence(comment)
        lowercase_words = []
        for w in words_after_filter:
            lowercase_words.append(w.lower())
 
        for kw in keywords:
            if kw["main_term"] in comment or kw["main_term"] in lowercase_words:
                if 'hits' not in kw:
                    kw["hits"] = 1
                else:
                    kw["hits"] += 1

                if comment_prevailing_emotion == "Happy":
                    if "happy_score" not in kw:
                        kw["happy_score"] = 1
                    else:
                        kw["happy_score"] += 1
                elif comment_prevailing_emotion == "Sad":
                    if "sad_score" not in kw:
                        kw["sad_score"] = 1
                    else:
                        kw["sad_score"] += 1
                elif comment_prevailing_emotion == "Fear":
                    if "fear_score" not in kw:
                        kw["fear_score"] = 1
                    else:
                        kw["fear_score"] += 1
                elif comment_prevailing_emotion == "Angry":
                    if "angry_score" not in kw:
                        kw["angry_score"] = 1
                    else:
                        kw["angry_score"] += 1
                elif comment_prevailing_emotion == "Surprise":
                    if "surprise_score" not in kw:
                        kw["surprise_score"] = 1
                    else:
                        kw["surprise_score"] += 1
             
        for word in lowercase_words:
            if word not in trending_keywords:
                trending_keywords[word] = 1
            else:
                trending_keywords[word] += 1
    for key in trending_keywords:
        score = trending_keywords[key]
        if score > 10:
            print(key + " had " + str(score) + " hits")
    return {
        "keywords": keywords,
        "trending_words": trending_keywords
    }

def keyword_info(keywords):
    infos = []
    for kw in keywords:
        infos.append({
            "main_term": kw["main_term"],
            "hits": kw.get("hits", 0),
            "happy_score": kw.get("happy_score", 0),
            "angry_score": kw.get("angry_score", 0),
            "fear_score": kw.get("fear_score", 0),
            "sad_score": kw.get("sad_score", 0),
            "surprise_score": kw.get("surprise_score", 0)
        })
    
    # Bubble sort
    did_swap = True
    while did_swap:

        swap_count = 0
        for index, item in enumerate(infos, start=1):
            if index == len(infos): # this is index out of bounds
                continue

            hits_prev = infos[index - 1]["hits"]
            hits_curr = infos[index]["hits"]
            if hits_curr > hits_prev:
                swap_count += 1
                infos[index], infos[index - 1] = infos[index - 1], infos[index]

        did_swap = swap_count > 0

    return infos

def map_trending_words(words, threshold):
    words_mapped = []
    for key in words:
        hits = words[key]
        if hits >= threshold:
           words_mapped.append(
                {
                    "value": key,
                    "hits": words[key]
                }
            ) 

    # Bubble sort
    did_swap = True
    while did_swap:

        swap_count = 0
        for index, item in enumerate(words_mapped, start=1):
            if index == len(words_mapped): # this is index out of bounds
                continue

            hits_prev = words_mapped[index - 1]["hits"]
            hits_curr = words_mapped[index]["hits"]
            if hits_curr > hits_prev:
                swap_count += 1
                words_mapped[index], words_mapped[index - 1] = words_mapped[index - 1], words_mapped[index]

        did_swap = swap_count > 0

    return words_mapped    

def filter_common_words_from_sentence(sentence):
    stop_words = set(stopwords.words('english'))
    punctuation = [".", ",", "'", ";", "!", "(", ")", "[", "]", "*", "&", "^", "%", "@", "#", "?", "$", "/", ":", "`", "|"]
    web_words = ["http", "https", "www"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    common_words = ["like", "would", "will", "get", "good", "know", "see", "still", "also", "well", "lot", "sure", "feel", "let"]
    word_tokens = word_tokenize(sentence)  
    filtered_sentence = []   
    for w in word_tokens:  
        w = w.lower()
        if (w not in stop_words and
            w not in punctuation and
            w not in web_words and 
            w not in numbers and
            "'" not in w and
            "\\u" not in w): 
            filtered_sentence.append(w)  
    return filtered_sentence

def print_emotion_results(results):
    happy_count = 0
    sad_count = 0
    angry_count = 0
    fear_count = 0
    surprise_count = 0
    for result in results:
        if result['Happy'] > 0.0:
            happy_count += 1
            
        if result['Sad'] > 0.0:
            sad_count += 1
        
        if result['Angry'] > 0.0:
            angry_count += 1
        
        if result['Fear'] > 0.0:
            fear_count += 1

        if result['Surprise'] > 0.0:
            surprise_count += 1
    print("------------------")
    print("For " + str(len(results)) + " emotion results")
    print("happy count: " + str(happy_count))
    print("sad count: " + str(sad_count))
    print("angry count: " + str(angry_count))
    print("fear count: " + str(fear_count))
    print("surprise count: " + str(surprise_count))
    print("------------------")
