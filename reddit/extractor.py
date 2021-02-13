
# Extracts body from comment and sub comments/replies
# TODO: might need to add something that grabs the 'more' comment(s)
def deep_extract_reply_bodies(comment):
    bodies = []

    if type(comment) is dict:
        comment_data = comment['data']
        if comment_data is not None:
            if 'replies' in comment_data and comment_data['replies'] != "":
                replies = comment_data['replies']['data']['children']

                for reply in replies:
                    if 'body' in reply['data']:
                        bodies.append(reply['data']['body'])

                    # recursively call this method to dig down into nested replies
                    bodies = bodies + deep_extract_reply_bodies(reply)
    return bodies

def deep_extract_replies_from_comments(comments):
    comment_bodies = []
    for comment in comments:
        # extract the comment body
        comment_data = comment['data']
        if comment_data is not None:
            if 'body' in comment_data: 
                comment_bodies.append(comment_data['body'])

        # dig down into the comment replies and add all the nested comment bodies
        comment_bodies = comment_bodies + deep_extract_reply_bodies(comment)
    return comment_bodies
