import requests

# By default, at most res will contain 100 posts.
#    but we can get more by calling the same url again, passing after={some_id}
#    num_pages_to_retrieve defines how many times to fetch the comments from the next `after` link    
# returns an array of comments (dicts) retrieved from the base_url
def retrieve_comment_data(base_url, path, json_indicator, request_headers, num_pages_to_retrieve):

    all_comments = []
    next_page_id = None
    for i in range(num_pages_to_retrieve):
        if next_page_id is not None:
            new_path = path + "&after=" + next_page_id
        else:
            new_path = path 

        res = requests.get(base_url + new_path, headers = request_headers)
        res = res.json()
        next_page_id = res["data"]["after"]

        print("Retrieving comments (page " + str(i + 1) + ")" , end = "", flush = True)
        comments = retrieve_child_comment_data(base_url, json_indicator, request_headers, res["data"]["children"])
        print(str(len(comments)) + " comments retrieved\n")
        all_comments = all_comments + comments

    return all_comments

# Takes the posts and retrieves the child comment data at their permalink.
# Returns the comment array containing all child comments
def retrieve_child_comment_data(base_url, json_indicator, request_headers, posts):
    comments = []
    for post in posts:
        print(".", end = "", flush = True)

        full_post_res = requests.get(base_url + post['data']['permalink'] + json_indicator, headers = request_headers)
        full_post_res = full_post_res.json()
        comments = comments + full_post_res[1]['data']['children']

    return comments

