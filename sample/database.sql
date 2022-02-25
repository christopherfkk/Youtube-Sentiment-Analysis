-- d_videos table definition

CREATE TABLE d_videos (
    id int NOT NULL AUTO_INCREMENT,
    video_id varchar(255),
    name varchar (255),
    views int,
    likes int,
    comments int,
    date date,
    PRIMARY KEY (id), 
    UNIQUE (video_id))

-- d_comments table definition

CREATE TABLE d_comments (
    id int NOT NULL AUTO_INCREMENT,
    video_id int,
    comment_id varchar(255),
    comment_raw varchar(5000),
    comment_clean varchar(5000),
    polarity decimal(5,3),
    sentiment varchar(255),
    PRIMARY KEY (id),
    FOREIGN KEY (video_id) REFERENCES d_videos (id),
    UNIQUE (comment_id))
        
-- upsert into d_videos

INSERT INTO
    d_videos(video_id, name, views, likes, comments, date)
VALUES
    { formatted_values } 
ON DUPLICATE KEY UPDATE id=id
    
-- upsert into d_comments with foreign key in d_videos

INSERT INTO
    d_comments (
        video_id,
        comment_id,
        comment_raw,
        comment_clean,
        polarity,
        sentiment
    )
VALUES
    { formatted_values } 
    ON DUPLICATE KEY UPDATE
    comment_raw = comment_raw
    comment_clean = comment_clean
    polarity = polarity
    sentiment = sentiment