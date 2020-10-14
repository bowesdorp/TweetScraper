# TweetScraper and Sentiment Analyser
This repository contains python scripts and tweet data for the group project: A collection organization website
for the course Information Organisation (5294INOR6Y). To run this project, first apply for developer access for
the twitter API (https://developer.twitter.com/en). Then put the access keys into the .envcopy file and rename
it to .env. Then simply run the tweetscraper script to start collecting the political tweets. Beware that the
sentiment analysis also converts the output to a .txt file that is in DynamoDB format
(https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.DataTypes.html).
