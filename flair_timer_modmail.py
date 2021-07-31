import praw
import config
import os.path
import json
import time
 
def authentication():
    print ("Authenticating...")
    reddit = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "Stronger1088's flair time notification bot. Made for /u/ScottishCrafter for his subreddits.")
    print ("Authenticated as {}.".format(reddit.user.me()))
    return reddit
 
def main(reddit, posts: dict):
    while True:
        for submission in reddit.subreddit(config.subreddit).new(limit=config.searchlimit):
            if not submission.saved:
                if submission.id not in posts.keys() and submission.link_flair_text == config.flair_text:
                    posts[submission.id] = time.time()
                    print(f"Post {submission} has been flaired {config.flair_text}")
                if submission.id in posts.keys() and submission.link_flair_text != config.flair_text:
                    posts.pop(submission.id)
                    print(f"Post {submission} has been unflaired {config.flair_text}")
 
        for submission in posts:
            if time.time() > posts[submission] + (config.hours * 60 * 60):
                posts.pop(submission)
                reddit.submission(submission).save()
                reddit.subreddit(config.subreddit).message(f"{config.messagetitle}", f"It has been {config.hours/24} day(s) since this was flaired [{config.flair_text}](https://reddit.com{reddit.submission(submission).permalink})")
                print(f"Post {submission} has been flaired {config.flair_text} for {config.hours/24} days, sent modmail")
                break
 
        save_posts(posts)
        time.sleep(config.interval)
 
def load_posts():
    if not os.path.exists("posts.json"):
        with open("posts.json", "w+") as file:
            json.dump({}, file)
    with open("posts.json", "r+") as file:
        data = json.load(file)
        return data
 
def save_posts(data):
    with open('posts.json', 'w+') as file:
        json.dump(data, file)
 
 
while True:
    try:
        posts = load_posts()
        main(reddit = authentication(), posts = posts)
    except Exception as e:
        print(e)
