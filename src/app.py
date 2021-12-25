from facebook_scraper import get_posts
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata, KafkaProducer
from datetime import datetime
import os
import json
from dotenv import load_dotenv
load_dotenv()

BOOSTRAP_SERVER = os.environ.get('BOOSTRAP_SERVER', '')
CONFIG_CONSUMER_ID = os.environ.get('CONFIG_CONSUMER_ID', '')
CONFIG_TOPIC = os.environ.get('CONFIG_TOPIC', '')
PAGE_ID = os.environ.get('PAGE_ID', '')
POST_TOPIC = os.environ.get('POST_TOPIC', '')
COOKIES_PATH = os.environ.get('COOKIE_PATH', '/opt/secret/cookies.json')

print("Starting up... ", datetime.now())

def get_last_message(consumer):
    try:
        partitions = consumer.partitions_for_topic(CONFIG_TOPIC)
        if partitions == None:
            return -1
        for partition in partitions:
            p = TopicPartition(CONFIG_TOPIC, partition)
            mypartition = [p]
            consumer.assign(mypartition)
            last_pos = consumer.end_offsets(mypartition)
            pos = last_pos[p]-1
            if pos == -1: 
                return 0
            offset = OffsetAndMetadata(pos, b'')
            consumer.commit(offsets={p: offset})
            
        return int(next(consumer).value.decode('utf-8'))
    except:
        return -1


consumer = KafkaConsumer(bootstrap_servers=BOOSTRAP_SERVER,
                         group_id=CONFIG_CONSUMER_ID,
                         auto_offset_reset='latest',
                         enable_auto_commit=False)

producer = KafkaProducer(bootstrap_servers=BOOSTRAP_SERVER)


last_post_id = get_last_message(consumer)
if last_post_id == -1:
    print("Error occured while getting offset")
    exit(1)
posts = []
facebook_posts = list(get_posts(PAGE_ID, pages=3))
print("Facebook Fetched Post: " + str(len(facebook_posts)))
for post in facebook_posts:
    current_post_id = post['post_id']
    post_timestamp = int(datetime.strptime(str(post['time']), '%Y-%m-%d %H:%M:%S').timestamp())
    if int(current_post_id) > int(last_post_id):
        posts.append({
            'post_id': post['post_id'],
            'text': post['text'],
            'image': post['image'],
            'image_lowquality': post['image_lowquality'],
            'post_url': post['post_url'],
            'username': post['username'],
            'shared_username': post['shared_username'],
            'shared_post_url': post['shared_post_url'],
            'shared_user_id': post['shared_user_id'],
            'time': str(post['time']),
            'timestamp': post_timestamp,
        })

def get_post_id(post):
    return post.get('post_id')

posts.sort(key=get_post_id)

print("Got " + str(len(posts)) + " post.")

if len(posts) <= 0:
    print("No new post available")
else :
    print("New post in total " + str(len(posts)))
    current_post_id = str(max(item['post_id'] for item in posts))
    for item in posts:
        print("Updating... " + str(item['post_id']))
        producer.send(POST_TOPIC, key=item['post_id'].encode('utf-8'), value=json.dumps(item).encode('utf-8')).get(timeout=30)
    producer.send(CONFIG_TOPIC, key=b'post_id', value=current_post_id.encode('utf-8')).get(timeout=30)
    print("Posts update completed.")