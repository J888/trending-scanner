import json
import os
import datetime; 

def report_data_with_source(data, source):
    return {
        "source": source,
        "data": data
    }

# data is a list of report data for each reddit topic
def generate_report_reddit(data):
    report_data = []
    timestamp = str(datetime.datetime.now()).replace(" ", "_")
    for item in data:

        report_data.append({
            "reported_at": timestamp,
            "source": item["subreddit"],
            "source_path": item["query_path"],
            "source_limit": item["limit"],
            "total_comments_analyzed": item["num_comments_analyzed"],
            "total_keywords": len(item["keywords"]), 
            "total_keyword_hits": item["total_keyword_hits"],
            "buzz": {
                "keywords": item["keywords"]
            },
            "other_trending": {
                "keywords": item["trending_words"]
            }
        })

    return report_data_with_source(report_data, "reddit")

# Writes a report in json containing all data
# returns the report file path
def write_report(report):
    timestamp = str(datetime.datetime.now()).replace(" ", "_")
    directory = "generated_reports"
    path = os.path.join(os.getcwd(), directory)

    if not os.path.isdir(path): # create only if the folder doesn't exist yet
        os.mkdir(path)

    filename = timestamp + ".json"
    file = open(directory + "/" + filename, "w+")

    json.dump(report, file)

    return path + "/" + filename
    