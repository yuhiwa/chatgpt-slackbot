# chatgpt-slackbot

## support only gpt3.5-turbo

## Features
- Conversation history is kept for each channel user individually, only if the response is less than 1 minute long
- set-chatgpt-system allows system role to be set, currently the same for all channel users
- unset-chatgpt-system can be used to set system role to empty, currently the same for all channel users
- system role can be checked with get-chatgpt-system
- Support in-thread behavior. (respond in-thread)

## Usage
- mention with question

## Setup

```
git clone https://github.com/yuhiwa/gpt3chat-slackbot.git
cd gpt3chat-slackbot
cp .env_sample .env
# open file .env and fill out your all api keys
docker-compose build
docker-compose up -d
```
