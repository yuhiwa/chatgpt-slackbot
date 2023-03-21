# chatgpt-slackbot

## gpt3.5-turboのみ対応

## 機能について
- 会話の履歴はチャンネル別ユーザ個別に1分以内の応答の場合にみ保持
- set-chatgpt-system で system role を設定できる、現在ここはすべてのチャンネルユーザで同一
- unset-chatgpt-system で system role 空に設定できる、現在ここはすべてのチャンネルユーザで同一
- get-chatgpt-system で system role を確認できる
- スレッド内での動作に対応(スレッド内応答する)

## 使い方
- メンションをつけて質問する

## セットアップ

```
git clone https://github.com/yuhiwa/gpt3chat-slackbot.git
cd gpt3chat-slackbot
cp .env_sample .env
# .envファイルにAPIキーを入力
docker-compose build
docker-compose up -d
```


