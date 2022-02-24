CREATE TABLE d_videos (
    id int NOT NULL AUTO_INCREMENT,
    video_id varchar(255),
    name varchar (255),
    views int,
    likes int,
    comments int,
    PRIMARY KEY (id)

CREATE TABLE d_comments (
    id int NOT NULL AUTO_INCREMENT,
    video_id int,
    comment_id varchar(255),
    comment_raw varchar(5000),
    comment_clean varchar(5000),
    polarity numeric,
    sentiment varchar(255),
    PRIMARY KEY (id),
    FOREIGN KEY (video_id) REFERENCES d_videos (id)

-- insert into d_comments with foreign key in d_videos

WITH ins (
    video_id,
    comment_id,
    comment_raw,
    comment_clean,
    polarity,
    sentiment
) AS (VALUE { formatted_values })
INSERT INTO
    d_comments (
        video_id,
        comment_id,
        comment_raw,
        comment_clean,
        polarity,
        sentiment
    )
SELECT
    d_videos.id,
    ins.comment_id,
    ins.comment_raw,
    ins.comment_clean,
    ins.polarity,
    ins.sentiment
FROM
    d_videos
    RIGHT JOIN ins ON ins.video_id = d_videos.id