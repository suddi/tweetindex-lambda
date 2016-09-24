# tweetindex-lambda

RESTful API to retrieve stock tweets about Fortune 100 stocks from Twitter's streaming API

## Requirements

Python 2.7 (At the time of writing this, AWS Lambda only supports Python 2.7).
Pip (~8.1.1)
Virtualenv (~15.0.0)
Virtualenvwrapper (~4.7.1)

## Setup

````
mkvirtualenv tweetindex-lambda

pip install -r requirements.txt
````

You will also need to setup the `~/.aws/credentials` file:

````
[default]
region = <AWS_REGION>
aws_access_key_id = <AWS_ACCESS_KEY_ID>
aws_secret_access_key = <AWS_SECRET_ACCESS_KEY>
````

## Usage

To test out the usage:

````
lambda invoke
````

To deploy to AWS lambda:

````
lambda deploy
````
