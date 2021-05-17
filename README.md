# Project summary

Our music streaming startup called Sparkify wants to migrate their data and processes to the cloud. 
We'll store the data on AWS S3 where song and user activity data is stored in JSON format.

This json data is loaded into a Redshift database into staging tables.
The staging tables are a copy of the json files. For our analysis purposes we copy the data into separate tables with song play, user, song etc. info.

# File summary

README.md - this is the file you're currently reading
dwh.cfg - contains configuration info, fill out the KEY and SECRET info as well as the IAM_ROLE
create_tables.py - run this in the terminal, it drops tables if they exist and creates new ones
etl.py - run this in the terminal. It pulls JSON data from S3 and loads it in staging tables, as well as copy from staging tables to analysis tables
start_stop_cluster.ipynb - convenience notebook using infrastructure-as-code snippets for starting and stopping the Redshift cluster
analysis.ipynb - convenience notebook for examining S3 data
sql_queries.py - all SQL queries for creating, copying data are contained in here

# Description of workflow

## Writing CREATE and DROP queries
Given the table descriptions in the project instructions I was able to write out the DROP and CREATE queries. For the types I copied them from the chapter 1 of the Udacity course (and changed serial to IDENTITY(0, 1) as the Redshift equivalent)
For the staging_events and staging_songs table I assume these will be COPY'd into the tables. The structure of these tables should match the structure of the files stored in the S3 bucket.
For the COPY I had to specify that the data is in a JSON format. For the events data the json paths are available.

## Determining table structure for staging tables
I have created a notebook to examine the contents of these files (see analysis.ipynb). To access them I have to specify my AWS account credentials which I have stored in the dwh.cfg under the [AWS] header, keys KEY and SECRET.

I examine json files in the log-data and song-data folders and determined the table structure from it.

### Example of log data:
{"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\\"Mozilla\\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/36.0.1985.143 Safari\\/537.36\\"","userId":"39"}

### Example of song data:
{"song_id": "SOBLFFE12AF72AA5BA", "num_songs": 1, "title": "Scream", "artist_name": "Adelitas Way", "artist_latitude": null, "year": 2009, "duration": 213.9424, "artist_id": "ARJNIUY12298900C91", "artist_longitude": null, "artist_location": ""}

## Copy from s3 into Redshift
To COPY the data from s3 into redshift the COPY statement needs an IAM_ROLE value for the ARN. 
I use the notebook supplied in chapter 2 (L3 Exercise 2 - IaC) to create the IAM role to get read access from redshift to the s3 bucket.
The supplied string I add into dwh.cfg under IAM_ROLE, ARN: arn:aws:iam::097733154984:role/dwhRole

