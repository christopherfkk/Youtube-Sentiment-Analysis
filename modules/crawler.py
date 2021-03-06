# pip install --upgrade google-api-python-client
# pip install --upgradpe google-auth-oauthlib google-auth-httplib2

from googleapiclient.discovery import build
from functools import lru_cache
from secret import *


class ApiCrawler():

    def __init__(self):
        """ 
        Initializes ApiCrawler instance with 10,000 units quote per day or 
        250,000 comments per day. E.g. a Joe Rogan podcast episode with Jordan
        Peterson has 89,925 comments + replies at 25,000,000 views
        """
        self.api_key = api_key

    @lru_cache  # retrieves cached output if arguments the same the second time
    def get_comments(self, video_id, n_requested):
        """ Gets the top-level comments of a single video and returns two arrays
        e.g. [ comment 1, comment 2, ...], [ comment_id 1, comment_id 2, ...]
        """
        comments = []
        ids = []

        youtube = build('youtube', 'v3', developerKey=self.api_key) # create youtube resource object

        # retrieve youtube video results
        video_response = youtube.commentThreads().list(
            part='snippet',
            maxResults=100,
            order="relevance",  # how comments are sorted, e.g. "time"
            videoId=video_id
        ).execute()

        while video_response:

            for item in video_response['items']:

                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                id = item['snippet']['topLevelComment']['id']

                comments.append(comment)
                ids.append(id)
            
            if 'nextPageToken' in video_response: # repeat if next page of comments exist

                if len(comments) >= n_requested: # don't repeat if larger than number of comments requested
                    video_response = False

                else:
                    video_response = youtube.commentThreads().list(
                        part='snippet, replies',
                        videoId=video_id,
                        pageToken=video_response['nextPageToken']
                    ).execute()

            else:
                video_response = False

        # print(f"actual number: {len(comments)}")
        # print(f"requested number: {n_requested}")

        return comments, ids

    @lru_cache
    def get_comments_and_replies(self, video_id, n_requested):
        """
        Gets the top-level comments and replies of a single video and returns a nested array of strings.
        E.g. [["first comment", ["first reply", "second reply"]], ["second comment", ["first reply", "second reply"], [third...]]]
        """

        comments_replies = []

        youtube = build('youtube', 'v3', developerKey=self.api_key) # create youtube resource object

        video_response = youtube.commentThreads().list(
            maxResults=100,
            part='snippet, replies',
            videoId=video_id
        ).execute()

        while video_response:

            for item in video_response['items']:

                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                replycount = item['snippet']['totalReplyCount']

                replies = []
                if replycount > 0:
                    for reply in item['replies']['comments']:
                        reply = reply['snippet']['textDisplay']
                        replies.append(reply)

                comments_replies.append([comment, replies])
            if 'nextPageToken' in video_response: # repeat if next page of comments exist

                if len(comments_replies) >= n_requested: # don't repeat if larger than number of comments requested
                    video_response = False

                else:
                    video_response = youtube.commentThreads().list(
                        part='snippet, replies',
                        videoId=video_id,
                        pageToken=video_response['nextPageToken']
                    ).execute()

            else:
                video_response = False

        # print(f"comment-reply bundle: {len(comments_replies)}")

        return comments_replies

    def get_stats(self, video_id):

        # create youtube resource object
        youtube = build("youtube", "v3", developerKey=self.api_key)

        # get the video statistics
        request = youtube.videos().list(part='snippet, statistics', id=video_id)
        response = request.execute()

        # return None if request has no result, e.g. private video
        if not response['items']:
            return None

        items = response['items'][0]

        name = items['snippet']['title']
        date = items['snippet']['publishedAt'].rpartition('T')[0]
        view_count = items['statistics']['viewCount']
        like_count = items['statistics']['likeCount']
        comment_count = items['statistics']['commentCount']

        return name, view_count, like_count, comment_count, date
