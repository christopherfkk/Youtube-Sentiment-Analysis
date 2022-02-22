CREATE TABLE d_videos (
    id int NOT NULL AUTO_INCREMENT,
    video_id varchar(255),
    name varchar (255),
    views int,
    likes int,
    dislikes int,
    comments int,
    PRIMARY KEY (id)
)

CREATE TABLE d_comments (
    id int NOT NULL AUTO_INCREMENT,
    comment_id varchar(255),
    comment_raw varchar(255),
    comment_clean varchar(255),
    polarity
)