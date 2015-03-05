import time
import praw
import re

r = praw.Reddit('Find Mills College mentions in local subreddits.')
recorded = []
# Find occurrences of "mills" other than "water mills" or "wind mills".
# Not used yet.
mills_mention = re.compile('^.*(?<!water\s)(?<!wind\s)mills.*$')
local_subreddits = ['test', 'oakland', 'bayarea', 'eastbay', 'sanfrancisco']

def write_to_log(sub):
	with open("mills_log.txt", "a") as log:
		print "Logging Mills entry into the file."
		log.write(time.strftime("%c"))
		log.write(": Found Mills @ %s\n" % sub.short_link)
		recorded.append(sub.id)

def check_this_subreddit(subreddit):
	subreddit = r.get_subreddit(subreddit)
	for submission in subreddit.get_hot(limit=10):
		op_text = submission.selftext.lower()

		# Checks if mills is mentioned in the OP text or in the title of the post.
		has_mills = "mills" in op_text or "mills" in submission.title
		if not has_mills:
			# Check comments of submission.
			nested_comments = submission.comments
			flat = praw.helpers.flatten_tree(nested_comments)
			for comment in flat:
				if "mills" in op_text or "mills" in submission.title:
					has_mills = True

		if has_mills and submission.id not in recorded:
			write_to_log(submission)



while True:
	for sub in local_subreddits: check_this_subreddit(sub)

	time.sleep(1800)