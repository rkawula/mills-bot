import time
import praw

r = praw.Reddit('Find Mills College mentions in local subreddits.')
#r.login()
recorded = []

def write_to_log(sub):
	with open("mills_log.txt", "a") as log:
		log.write(time.strftime("%c"))
		log.write(": Found Mills @ %s\n"  % sub.short_link)
		recorded.append(sub.id)
		log.flush()
		log.close()

def check_this_subreddit(subreddit):
	subreddit = r.get_subreddit(subreddit)
	for submission in subreddit.get_hot(limit=10):
		op_text = submission.selftext.lower()
		has_mills = "mills" in op_text or "mills" in submission.title

		if submission.id not in recorded and has_mills:
			write_to_log(submission)

while True:
	check_this_subreddit('oakland')
	check_this_subreddit('bayarea')
	check_this_subreddit('eastbay')
	check_this_subreddit('sanfrancisco')

	time.sleep(1800)