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
submission_url = 'https://www.reddit.com/r/wallstreetbets/comments/1ipdac5/weekly_earnings_thread_217_221/'  # TODO: Change to search for latest weekly thread

# Fetch the submission (post)
submission = reddit.submission(url=submission_url)

# Ensure you retrieve all nested comments (not just top-level ones)
submission.comments.replace_more(limit=None)

def combine_comments(comment, separator=" | "):
    combined = comment.body.strip().replace('\n', ' ')
    if hasattr(comment, 'replies'):
        replies_text = []
        for reply in comment.replies:
            if isinstance(reply, praw.models.Comment):
                replies_text.append(combine_comments(reply, separator))
        if replies_text:
            combined += separator + separator.join(replies_text)
    return combined

# Process each top-level comment and combine its nested replies
combined_comments = []
for top_comment in submission.comments:
    if isinstance(top_comment, praw.models.Comment):
        combined_text = combine_comments(top_comment)
        combined_comments.append(combined_text)

# Define sentiment words
positive_words = ["long", "call", "calls"]
negative_words = ["short", "put", "puts"]

positive_count = 0
negative_count = 0

# Store filtered comments (those that mention the stock)
filtered_comments = []

# Filter comments that mention "block" or "XYZ" (case-insensitive) and accumulate sentiment counts
for comment_text in combined_comments:
    lower_text = comment_text.lower()
    if "Rivian" in lower_text or "RIVN" in lower_text:
        filtered_comments.append(comment_text)
        # Count occurrences of positive sentiment words
        for pos in positive_words:
            pos_occurrences = lower_text.count(pos)
            if pos_occurrences > 0:
                positive_count += pos_occurrences
                print(f"Found positive sentiment word '{pos}' {pos_occurrences} times in comment. Total positive count: {positive_count}")
        # Count occurrences of negative sentiment words
        for neg in negative_words:
            neg_occurrences = lower_text.count(neg)
            if neg_occurrences > 0:
                negative_count += neg_occurrences
                print(f"Found negative sentiment word '{neg}' {neg_occurrences} times in comment. Total negative count: {negative_count}")

# Output sentiment analysis results
print("\nSentiment Analysis:")
print(f"Positive sentiment count: {positive_count}")
print(f"Negative sentiment count: {negative_count}")
