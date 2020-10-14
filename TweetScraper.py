# import the necessarily libraries
import os
import dotenv
import tweepy
import csv

# gather the access keys from .env
dotenv.load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_KEY_SECRET = os.getenv('CONSUMER_KEY_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Main script that runs the tweet scraper
if __name__ == '__main__':

    # Initialize the tweet scraper
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Headers and party dataand queries
    headers = ['username', 'following',
               'followers', 'totaltweets', 'tweetcreatedts',
               'query', 'text', 'retweet', 'party', 'targeted']

    parties = {
        'VVD': {
            'queries': ['@VVD', '#VVD', '@markrutte', '#markrutte']
        },
        'PVV': {
            'queries': ['@PVV', '#PVV', '@geertwilderpvv', '#geertwilders']
        },
        'CDA': {
            'queries': ['@cdavandaag', '#CDA', '@hugodejonge', '#hugodejonge']
        },
        'D66': {
            'queries': ['@D66', '#D66', '@SigridKaag', '#sigridkaag']
        },
        'GL': {
            'queries': ['@groenlinks', '#groenliinks', '@jesseklaver', '#jesseklaver']
        },
        'SP': {
            'queries': ['@SPnl', '#SP', '@MarijnissenL', '#lilianmarijnissen']
        },
        'PVDA': {
            'queries': ['@PvdA', '#PvdA', '@LodewijkA', '#lodewiijkasscher']
        },
        'CU': {
            'queries': ['@christenunie', '#christenunie', '@gertjansegers', '#gertjansegers']
        },
        'PVVD': {
            'queries': ['@PartijvdDieren', '#PvdD', '@estherouwehand', '#estherouwehand']
        },
        '50PLUS': {
            'queries': ['@50pluspartij', '#50plus', '@LianedenHaan', '#lianedenhaan']
        },
        'SGP': {
            'queries': ['@SGPnieuws', '#SGP', '@keesvdstaaij', '#keesvanderstaaij']
        },
        'DENK': {
            'queries': ['@DenkNL', '#Denk', '@F_azarkan', '#faridazarkan']
        },
        'FVD': {
            'queries': ['@fvdemocratie', '#FvD', '@thierrybaudet', '#thierrybaudet']
        },
        'PVDT': {
            'queries': ['@partij_toekomst', '#PvdT', '@HenkKrol', '#henkkrol']
        }

    }

    count = 1000
    tweets_list = []

    with open('./data/ALLPARTIES.csv', mode='w') as wf:
        all_writer = csv.writer(wf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        all_writer.writerow(headers)
        for party in parties:
            with open('./data/' + party + '.csv', mode='w') as f:
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(headers)
                # Determines if the tweet is directed at the party or the leader
                target = 1
                for query in parties[party]['queries']:
                    nr_of_tweet = 1
                    print('Current query: ', query)
                    # Creation of query method using parameters
                    c = tweepy.Cursor(api.search, q=query, lang="nl", tweet_mode="extended",
                                      include_entities=True).items(count)
                    for tweet in c:
                        # Pull the values
                        username = tweet.user.screen_name
                        following = tweet.user.friends_count
                        followers = tweet.user.followers_count
                        totaltweets = tweet.user.statuses_count
                        tweetcreatedts = tweet.created_at
                        retweet = 'Yes'

                        # Check if a tweet is a retweet or not
                        try:
                            tweet_text = tweet.retweeted_status.full_text
                            retweet = True
                        except AttributeError:  # Not a Retweet
                            tweet_text = tweet.full_text

                        # filter trailing whitespaces
                        split_tweet = [line for line in tweet_text.split('\n') if line.strip() != '']
                        text = "".join(split_tweet)

                        if target > 2:
                            targeted = 'leader'
                        else:
                            targeted = 'party'

                        all_data = [username, following, followers, totaltweets,
                                    tweetcreatedts, query, text, retweet, party, targeted
                                    ]
                        csv_writer.writerow(all_data)
                        all_writer.writerow(all_data)
                        print('New row:  ', nr_of_tweet, ' for: ', query)
                        nr_of_tweet += 1
                    target += 1
