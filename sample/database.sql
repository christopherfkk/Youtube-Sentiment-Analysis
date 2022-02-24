CREATE TABLE d_videos (
    id int NOT NULL AUTO_INCREMENT,
    video_id varchar(255),
    name varchar (255),
    views int,
    likes int,
    comments int,
    PRIMARY KEY (id)
)

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
)