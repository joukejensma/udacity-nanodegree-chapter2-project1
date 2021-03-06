import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES
staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events
(
artist varchar,
auth varchar not null,
firstName varchar,
gender varchar,
itemInSession varchar not null,
lastName varchar,
length varchar,
level varchar not null,
location varchar,
method varchar not null,
page varchar not null,
registration varchar,
sessionId varchar not null,
song varchar,
status varchar not null,
ts varchar not null,
userAgent text,
userId integer
)
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs
(
song_id varchar not null,
num_songs varchar not null,
title varchar not null,
artist_name varchar not null,
artist_latitude double precision,
year integer not null,
duration double precision,
artist_id varchar not null,
artist_longitude double precision,
artist_location varchar
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays
(
songplay_id integer identity(0,1), 
start_time varchar NOT NULL, 
user_id varchar NOT NULL, 
level varchar NOT NULL, 
song_id varchar, 
artist_id varchar, 
session_id varchar NOT NULL, 
location varchar, 
user_agent varchar NOT NULL, 
primary key (songplay_id)
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users
(
user_id integer primary key NOT NULL,
first_name varchar NOT NULL, 
last_name varchar NOT NULL, 
gender varchar NOT NULL, 
level varchar NOT NULL
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs
(
song_id varchar, 
title varchar NOT NULL, 
artist_id varchar NOT NULL, 
year int NOT NULL, 
duration numeric NOT NULL, 
primary key(song_id)
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists
(
artist_id varchar, 
name varchar NOT NULL, 
location varchar, 
latitude numeric, 
longitude numeric, 
primary key(artist_id)
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time
(
start_time timestamp NOT NULL, 
hour int NOT NULL, 
day int NOT NULL, 
week int NOT NULL, 
month int NOT NULL, 
year int NOT NULL, 
weekday int NOT NULL, 
primary key(start_time)
)
""")

# STAGING TABLES
staging_events_copy = ("""
COPY staging_events FROM '{}'
CREDENTIALS 'aws_iam_role={}'
format as json '{}'
region 'us-west-2';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
COPY staging_songs FROM '{}'
CREDENTIALS 'aws_iam_role={}'
region 'us-west-2'
json 'auto';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES
songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT e.ts as start_time, e.userId as user_id, e.level, s.song_id, s.artist_id, e.sessionId as session_id, e.location, e.userAgent as user_agent 
FROM staging_events e
JOIN staging_songs s ON (e.song = s.title)
WHERE e.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT e.userId as user_id, e.firstName as first_name, e.lastName as last_name, e.gender, e.level
FROM staging_events e
WHERE e.userId IS NOT NULL
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT s.song_id, s.title, s.artist_id, s.year, s.duration
FROM staging_songs s
""")

artist_table_insert = ("""
INSERT INTO artists
(artist_id, name, location, latitude, longitude)
SELECT DISTINCT s.artist_id, s.artist_name as name, s.artist_location as location, s.artist_latitude as latitude, s.artist_longitude as longitude
FROM staging_songs s
""")

time_table_insert = ("""
INSERT INTO time 
(start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT TIMESTAMP 'epoch' + e.ts/1000 * INTERVAL '1 second' as start_time,
EXTRACT(HOUR FROM start_time) as hour, 
EXTRACT(DAY FROM start_time) as day,
EXTRACT(WEEK FROM start_time) as week,
EXTRACT(MONTH FROM start_time) as month,
EXTRACT(YEAR FROM start_time) as year,
EXTRACT(WEEKDAY FROM start_time) as weekday
FROM
staging_events e
""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
