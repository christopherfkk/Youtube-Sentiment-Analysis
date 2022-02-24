from modules.dbconnector import DBConnector
from modules.crawler import ApiCrawler
from modules.analyzer import CommentAnalyzer

videos = ['ycPr5-27vSI', '-5yh2HcIlkU', 'efs3QRr8LWw', 'BEWz4SXfyCQ', 'RcYjXbSJBN8',
          'jdVso9FSkmE', '6T7pUEZfgdI', '7MNv4_rTkfU', 'vGc4mg5pul4', 'UQTfyjhvfH8']
videos = ['ycPr5-27vSI']


def insert_comments(video_lst):
    """ id (auto) | video_id | comment_id | comment_raw | comment_clean | polarity | sentiment """

    crawler = ApiCrawler()
    db = DBConnector()

    values = []

    for video_id in video_lst:
        comments, ids = crawler.get_comments(video_id, 100)

        for i in range(len(comments)):

            analyzer = CommentAnalyzer(comments[i])
            value = tuple([video_id, ids[i], comments[i], analyzer.clean(), analyzer.get_polarity(), analyzer.get_sentiment()])
            values.append(value)

    formatted_values = str(values)[1:-1]
    print(formatted_values)
    #db.execute_sql_query(f"WITH ins (video_id, comment_id, comment_raw, comment_clean, polarity, sentiment) AS (VALUE {formatted_values} INSERT INTO d_comments ( video_id, comment_id, comment_raw, comment_clean, polarity, sentiment SELECT d_videos.id, ins.comment_id, ins.comment_raw, ins.comment_clean, ins.polarity, ins.sentimen FROM d_videos RIGHT JOIN ins ON ins.video_id = d_videos.id")


def insert_videos(video_lst):
    """ id (auto) | video_id | name | views | likes | comments | date"""

    crawler = ApiCrawler()
    db = DBConnector()

    values = []
    for video_id in video_lst:
        name, view_count, like_count, comment_count, date = crawler.get_stats(video_id)
        value = tuple([video_id, name, view_count, like_count, comment_count, date])
        values.append(value)

    formatted_values = str(values)[1:-1]
    db.execute_sql_query(f"INSERT INTO d_videos(video_id, name, views, likes, comments, date) VALUES {formatted_values}")

insert_comments(videos)