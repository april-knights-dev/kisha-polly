import os
import logging
from logging import Logger
import traceback
from datetime import datetime

from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App, Ack, BoltResponse, Respond
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Callable

from blocks import BlocksChangeMessage

logging.basicConfig(level=logging.INFO)

# export SLACK_BOT_TOKEN=xoxb-***
# export SLACK_SIGNING_SECRET=***
app = App()

# flaskベースで実行するためのハンドラー
# debugに便利なのでflaskベースのままで実行推奨
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)
usergroup_id = "S040T3YQVK4"  # ユーザグループ変更することがあれば書き換えてください


# リスナーのログと同時に見るためにペイロードを標準出力に表示するだけのmiddleware
@app.use
def log_request(logger: Logger, body: dict, next: Callable[[], BoltResponse]):
    logger.info(body)
    next()


# スラッシュコマンドのリスナー
@app.command("/kisyabi")
def tell_response_url(ack: Ack, body: dict, respond: Respond, logger: Logger):
    logger.info("スラッシュコマンド実行")
    assert body.get("response_url") is not None
    ack()
    change_message = BlocksChangeMessage()

    # 西暦取得
    AD = datetime.now().year

    # ex. 12/24 -> 12_24_帰社日
    date_number = body["text"].split("/")
    channel_name = f"{AD}_{date_number[0]}_{date_number[1]}_帰社日"

    try:
        # チャンネル作成
        channel_careated_response = client.conversations_create(name=channel_name, is_private=True)
        channel_id = channel_careated_response["channel"]["id"]
        logger.info(f"チャンネル作成完了：{channel_id}")

        # チャンネルIDと帰社日の日付を変更したblocksを生成
        change_message.blocks_change_date(body["text"])
        change_message.blocks_add_channelid(channel_id)
        respond(blocks=change_message.blocks_format["blocks"], response_type="in_channel")
        
    except SlackApiError:
        traceback.print_exc()
    

@app.action("join")
def action_button_click(body: dict, ack: Ack, respond: Respond, logger: Logger):
    ack()
    try:
        # slackから送られてくるペイロードにblocksの情報が入っているのでそこからchannelidを取得
        channel_id = body["message"]["blocks"][4]["elements"][0]["text"]
        logger.info(f"利用するチャンネルID：{channel_id}")

        # ボタンを押したユーザをチャンネルに招待
        client.conversations_invite(channel=channel_id, users=[body['user']['id']])
        logger.info(f"{body['user']['username']}が参加")
    
    except Exception:
        traceback.print_exc()


@app.action("close")
def action_button_click(body: dict, ack: Ack, respond: Respond, logger: Logger):
    ack()
    access_user_id = body['user']['id']
    allow_users_id = client.usergroups_users_list(usergroup=usergroup_id)['users']

    if access_user_id in allow_users_id:
        respond("帰社日参加の募集は終了しました")
    else:
        logger.warn(f"実行許可のないユーザが実行しました：ID-{body['user']['id']}:USERNAME-{body['user']['username']}")


# flask->bolt
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


if __name__ == "__main__":
    # 検証時にはdebug=Trueにすると便利
    flask_app.run(port=8080, debug=False)
