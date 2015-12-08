# /usr/bin/python3
import praw
import csv
import time

if __name__ == "__main__":
	r = praw.Reddit(user_agent='cs-383-project')
	maxsub = 10
	current_time = int(time.time())
	with open('test.csv', 'wb') as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerow(['Score', 'Title', 'Author', 'Subreddit', 'Domain', 'Self Post?', 'NSFW', 'Age of Submission (Days)'])
		posts = r.get_random_submission(limit=maxsub)
		for x in posts:
			print str(x)+"\n"
			age = ((current_time - x.created_utc) / 60 / 60 / 24)
			if (age > 1 or x.score > 500):
				a.writerow([x.score, x.title, x.author, x.subreddit, x.domain, x.is_self, x.over_18, age])