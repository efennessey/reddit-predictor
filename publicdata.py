import praw
import csv
import time
import random
import os

if __name__ == "__main__":

	r = praw.Reddit(user_agent='cs-383-project')
	statinfo = os.stat('../publicvotes.csv')
	count = 0

	with open('lotsadata.csv', 'wb') as ld:
		writer = csv.writer(ld, delimiter=',')
		#writer.writerow(['Class', 'Score', 'Title', 'Author', 'Subreddit', 'Domain', 'Self Post?', 'NSFW', 'SubmissionID'])
		for x in range(0, 1000):
			offset = random.randrange(statinfo.st_size)
			f = open('../publicvotes.csv')
			f.seek(offset)
			f.readline()
			random_line = f.readline()
			if len(random_line) == 0:
				f.seek(0)
				random_line = f.readline()
			a = random_line.find(",t3_")
			end_line = random_line[a+4:]
			link, junk = end_line.split(",", 1)
			post = r.get_submission(submission_id=link)

			# Our classification here:
			if post.score >= 1500:
				classification = 2
			elif post.score < 500:
				classification = 0
			else:
				classification = 1

			writer.writerow([classification, post.score, post.title.encode('ascii', 'ignore'), post.author, post.subreddit, post.domain, post.is_self, post.over_18, link])
			count += 1
			print str(count)+': '+str(post.title.encode('ascii', 'ignore'))