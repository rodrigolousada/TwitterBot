# Retrieve and Store from file
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# Reply to Tweet function
def reply_to_tweets(api, file_name):
    mentions = api.mentions_timeline()

    # print("Mentions keys are: ", mentions[0].__dict__.keys())
    # print("Last mention was: ", mentions[0].text)
    # print("Last mention id: ", mentions[0].id)
    # print("Type of last last mention id: ", type(mentions[0].id))

    FILE_NAME = file_name

    print("retrieving and replying to tweets...")
    #DEV NOTE: for TEST purpose use 376831330887036928 in last_seen_id.txt
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#helloworld' in mention.full_text.lower():
            print("found #helloworld!", flush=True)
            print("responding back...", flush=True)
            api.update_status('@' + mention.user.screen_name
                              + ' Hello World is a good hashtag!', mention.id)
        