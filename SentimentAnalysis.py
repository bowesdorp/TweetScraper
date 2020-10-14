import pandas as pd
import emoji
import json
from decimal import Decimal
from boto3.dynamodb.types import TypeSerializer
from textblob import TextBlob
from textblob_nl import PatternTagger, PatternAnalyzer

# Path to file
path = './data/ALLPARTIES.csv'
headers = ['id', 'username', 'following', 'followers', 'totaltweets', 'tweetcreatedts', 'query', 'text', 'retweet',
           'party', 'targeted', 'polarity', 'subjectivity']


# Filters all emojis from a string
def ef(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text


# Main script to perform sentiment analysis and converting the rows to a workable format for DynamoDB
if __name__ == '__main__':
    df = pd.read_csv(path)
    typer = TypeSerializer()
    count = 1
    with open('./results/annotated_data.txt', mode='w') as f:
        for index, row in df.iterrows():

            # Filter the text from the tweet
            text = ef(row['text'])

            # Perform sentiment analysis
            blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
            polarity = blob.sentiment[0]
            subjectivity = blob.sentiment[1]

            td = {
                "Id": count,
                "Username": ef(row['username']),
                "Following": int(row['following']),
                "Followers": int(row['followers']),
                "Totaltweets": int(row['totaltweets']),
                "Tweetcreatedts": row['tweetcreatedts'],
                "Query": row['query'],
                "Text": text,
                "Retweet": row['retweet'],
                "Party": row['party'],
                "Targeted": row['targeted'],
                "Polarity": polarity,
                "Subjectivity": subjectivity,
            }

            # Convert rows to workable values for DynamoDB
            t = json.loads(json.dumps(td), parse_float=Decimal)
            dbb = json.dumps(typer.serialize(t)['M'])
            dbb = dbb.replace('"M"', '"m"')
            dbb = dbb.replace('"L"', '"l"')
            dbb = dbb.replace('"S"', '"s"')
            dbb = dbb.replace('"N"', '"n"')

            f.write(dbb)
            f.write('\n')
            count += 1

