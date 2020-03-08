import requests
import json
# url='https://twitter.com/Ding1204'
# url='https://twitter.com/NBA'
proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'https://127.0.0.1:1080',
}

# url='https://api.twitter.com/2/timeline/profile/19923144.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweets=true&include_tweet_replies=false&userId=19923144&count=20&cursor=HBaEgLvNu7WcqCIAAA%3D%3D&ext=mediaStats%2ChighlightedLabel%2CcameraMoment'
# url='https://api.twitter.com/2/timeline/profile/1193116782501826561.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweets=true&include_tweet_replies=false&userId=19923144&count=20&cursor={}&ext=mediaStats%2ChighlightedLabel%2CcameraMoment'
url='https://api.twitter.com/2/timeline/profile/1070623326035460096.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=0&include_want_retweets=0&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweets=false&include_tweet_replies=false&userId=1070623326035460096&count=20&cursor={}&ext=mediaStats%2ChighlightedLabel%2CcameraMoment'
url='https://api.twitter.com/2/timeline/media/1070623326035460096.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweets=true&count=20&cursor={}&ext=mediaStats%2ChighlightedLabel%2CcameraMoment'
headers={
    # "authority": "api.twitter.com",
    # "method": "GET",
    # "accept": "*/*",
    # "scheme": "https",
    # "accept-encoding": "gzip, deflate, br",
    # "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    # "cookie": "_ga=GA1.2.1293086995.1583258930; kdt=p60OexkxvFn4oAwMX2lPWuAhjvOtPad1AqePUQNO; remember_checked_on=1; csrf_same_site_set=1; csrf_same_site=1; tfw_exp=0; ct0=39ca5216c2bc93f6c5d54c7062250ef5; _gid=GA1.2.2137799834.1583665696; dnt=1; personalization_id='v1_0YOUwaZol884hj5NjtzIlw=='; guest_id=v1%3A158366810763053821; gt=1236619789017083905; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCCe%252BblwAToMY3NyZl9p%250AZCIlNmNiZWZiZjdiYjk2M2UyMTM3Yzg2NWM4OWU1NzU1Njc6B2lkIiU3OTA4%250AMzA5MTViMjYxZDUyZDAzNjdmNWNlNTRhYmJjZQ%253D%253D--22f528d3e1655bce53340addcdc06e8d462b4487",
    # "cookie": "_ga=GA1.2.1293086995.1583258930; kdt=p60OexkxvFn4oAwMX2lPWuAhjvOtPad1AqePUQNO; remember_checked_on=1; csrf_same_site_set=1; csrf_same_site=1; tfw_exp=0; ct0=39ca5216c2bc93f6c5d54c7062250ef5; _gid=GA1.2.2137799834.1583665696; dnt=1; personalization_id='v1_0YOUwaZol884hj5NjtzIlw=='; guest_id=v1%3A158366810763053821; gt=1236619789017083905; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCCe%252BblwAToMY3NyZl9p%250AZCIlNmNiZWZiZjdiYjk2M2UyMTM3Yzg2NWM4OWU1NzU1Njc6B2lkIiU3OTA4%250AMzA5MTViMjYxZDUyZDAzNjdmNWNlNTRhYmJjZQ%253D%253D--22f528d3e1655bce53340addcdc06e8d462b4487",
    "cookie": "_ga=GA1.2.1293086995.1583258930; kdt=p60OexkxvFn4oAwMX2lPWuAhjvOtPad1AqePUQNO; csrf_same_site_set=1; csrf_same_site=1; tfw_exp=0; ct0=39ca5216c2bc93f6c5d54c7062250ef5; _gid=GA1.2.2137799834.1583665696; dnt=1; personalization_id='v1_0YOUwaZol884hj5NjtzIlw=='; guest_id=v1%3A158366810763053821; gt=1236619789017083905; external_referer=padhuUp37zgetdc93twWEFQ%2FDqS1HEb4||8e8t2xd8A2w%3D; ads_prefs='HBESAAA='; remember_checked_on=0; _twitter_sess=BAh7DCIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCCe%252BblwAToMY3NyZl9p%250AZCIlNmNiZWZiZjdiYjk2M2UyMTM3Yzg2NWM4OWU1NzU1Njc6B2lkIiU3OTA4%250AMzA5MTViMjYxZDUyZDAzNjdmNWNlNTRhYmJjZTofbG9naW5fdmVyaWZpY2F0%250AaW9uX3VzZXJfaWRsKwkB0NRJg1L0DjoibG9naW5fdmVyaWZpY2F0aW9uX3Jl%250AcXVlc3RfaWQiK1lPZ0JGNkQwZkF6eGZkS0YzdVBlNUVkaUZDUnVXcmtnTXEz%250AS0FrOgl1c2VybCsJAdDUSYNS9A4%253D--6b5e938af61d7fc1aeb6f84d80e62a5326d7ebec; auth_token=abf922de7a1ce681513ad28c556319682bf9cfdd; rweb_optin=side_no_out; twid=u%3D1077576934681268225",
    # "origin": "https://twitter.com",
    # "referer": "https://twitter.com/NBA",
    # "sec-fetch-dest": "empty",
    # "sec-fetch-mode": "cors",
    # "sec-fetch-site": "same-site",
    # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    "x-csrf-token": "39ca5216c2bc93f6c5d54c7062250ef5",
    "x-guest-token": "1236619789017083905",
    # "x-twitter-active-user": "yes",
    # "x-twitter-client-language": "zh-cn",
}
# cursor='HCaAgIDo2Pi4qSIAAA=='
cursor='HBaCwKDJit%2FGlCAAAA%3D%3D'
cursor='HBaAwKLJjZWwrCEAAA%3D%3D'
for i in range(5):

    res=requests.get(url=url.format(cursor),proxies=proxies,headers=headers).json()
    # data=json.dumps(res,indent=4)
    # print(data)
    # print(res)
    tweets = res.get('globalObjects').get('tweets')

    for tweet in tweets.values():
        # print(tweet)
        onetweet=tweet
        break
    break
        # print(tweet.get('full_text'))
    cursor = res['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
    # instructions=json.dumps(instructions,indent=4)
    print(cursor)

    # print(res['timeline']['instructions']['addEntries']['entries'][-1])

onetweet=json.dumps(onetweet,indent=4)
print(onetweet)


