# Facebook Page Scraper
## Get the page post and sink in to kafka

This software built specific on purpose to sink the new facebook post to kafka

## Plugins

| Name | Description |
| ------ | ------ |
| BOOSTRAP_SERVER | Kafka boostrap server |
| CONFIG_CONSUMER_ID | Consumer id for the config topic |
| CONFIG_TOPIC | Topic that use for keep track the latest post |
| POST_TOPIC | Topic that you want to sink the post to |
| PAGE_ID | Facebook page id  (https://www.facebook.com/**PAGEID**) |


## Docker
*Note: This docker image design to run as cronjob in kubernetes, When it finish the container will exit
```sh
docker pull takumiproducer/facebook-kafka-scraper:1.2
docker run -e ENV=VALUE takumiproducer/facebook-kafka-scraper
```

## License

MIT

# Reference
This software use the facebook-scraper from **kevinzg/facebook-scraper**