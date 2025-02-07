import praw

print("start")

# Replace these with your credentials from the Reddit app
# FIXME: Make sure ID/SECRET is hidden for GitHub
CLIENT_ID = '7L-O0GuqSiF7vlkJYB7I1A'
CLIENT_SECRET = 'xfjE_b_yK6z9xTpCJcrlvatcnsC8SA'
USER_AGENT = 'WallstreetbetsScraper'

# Initialize the Reddit instance
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

# Provide the URL of the Reddit post (discussion) you want to scrape
submission_url = 'https://www.reddit.com/r/wallstreetbets/comments/1ijxkzt/weekly_earnings_thread_210_214/'  # TODO: Change to search for latest weekly thread

# Fetch the submission (post)
submission = reddit.submission(url=submission_url)

# Ensure you retrieve all nested comments (not just top-level ones)
submission.comments.replace_more(limit=None)

def combine_comments(comment, separator=" | "):
    """
    Recursively combines a comment's body with its replies into one single line.
    Newlines within each comment are removed so that the output is on one line.
    
    Args:
        comment (praw.models.Comment): A Reddit comment object.
        separator (str): The string to insert between comment levels.
    
    Returns:
        str: The combined comment text.
    """
    # Remove extra whitespace and newlines from the comment text
    combined = comment.body.strip().replace('\n', ' ')
    
    # Process each reply recursively if available
    if hasattr(comment, 'replies'):
        replies_text = []
        for reply in comment.replies:
            # Make sure we're only processing actual comments (skip MoreComments if any)
            if isinstance(reply, praw.models.Comment):
                replies_text.append(combine_comments(reply, separator))
        if replies_text:
            # Append the replies to the original comment text using the separator
            combined += separator + separator.join(replies_text)
    return combined

# Process each top-level comment and combine its nested replies
combined_comments = []
for top_comment in submission.comments:
    # Ensure it's a proper comment object
    if isinstance(top_comment, praw.models.Comment):
        combined_text = combine_comments(top_comment)
        combined_comments.append(combined_text)

print(f"Total top-level threads found: {len(combined_comments)}\n")

# Display each combined comment thread
for comment_text in combined_comments:
    print(comment_text)
    print('-' * 60)
