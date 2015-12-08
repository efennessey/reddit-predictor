# /usr/bin/python3
import praw
import csv
import time

if __name__ == "__main__":
	r = praw.Reddit(user_agent='cs-383-project')
	maxsub = 100
	current_time = int(time.time())
	with open('test.csv', 'wb') as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerow(['Score', 'Title', 'Author', 'Subreddit', 'Domain', 'Self Post?', 'NSFW', 'Age of Submission (Days)'])
		for x in range(0, maxsub):
			post = r.get_random_submission()
			age = ((current_time - post.created_utc) / 60 / 60 / 24)
			print "Age: "+str(age)+"\n"
			#if (age > 0.25 or post.score > 500):
			a.writerow([post.score, str(post.title), post.author, post.subreddit, post.domain, post.is_self, post.over_18, age])