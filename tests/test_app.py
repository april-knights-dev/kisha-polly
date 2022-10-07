import unittest
import os
import traceback

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.app import action_button_click


class TestApp(unittest.TestCase):

    def test_app_join_button(self):
        slack_token = os.environ["SLACK_BOT_TOKEN"]
        client = WebClient(token=slack_token)

        channel_id = "C045H94R7EU"
        print("channel_id:", channel_id)

        # このペイロードだとchannel_not_foundが出るのでテストするときは注意
        test_payload = {'actions': [{'action_id': 'join',
                    'action_ts': '1665116856.817162',
                    'block_id': 'DpXrT',
                    'style': 'primary',
                    'text': {'emoji': True, 'text': '参加', 'type': 'plain_text'},
                    'type': 'button',
                    'value': 'click_me_123'}],
        'api_app_id': 'A043MPCTEP5',
        'channel': {'id': 'C9R61S3B4', 'name': 'all_全体連絡'},
        'container': {'channel_id': 'C9R61S3B4',
                    'is_ephemeral': False,
                    'message_ts': '1664764453.264719',
                    'type': 'message'},
        'enterprise': None,
        'is_enterprise_install': False,
        'message': {'blocks': [{'block_id': 'Z23hS',
                                'text': {'emoji': True,
                                        'text': '帰社日のご連絡',
                                        'type': 'plain_text'},
                                'type': 'header'},
                                {'block_id': '/GAVy',
                                'text': {'text': '次回の帰社日は10/280になります。\\n参加される方は「 *参加* '
                                                '」のボタンを押してください',
                                        'type': 'mrkdwn',
                                        'verbatim': False},
                                'type': 'section'},
                                {'block_id': 'DpXrT',
                                'elements': [{'action_id': 'join',
                                            'style': 'primary',
                                            'text': {'emoji': True,
                                                        'text': '参加',
                                                        'type': 'plain_text'},
                                            'type': 'button',
                                            'value': 'click_me_123'}],
                                'type': 'actions'},
                                {'block_id': 'E5PR',
                                'text': {'text': '*※以下管理者のみ実行可能*',
                                        'type': 'mrkdwn',
                                        'verbatim': False},
                                'type': 'section'},
                                {'block_id': 'AYL',
                                'elements': [{'emoji': True,
                                            'text': 'C045H94R7EU',
                                            'type': 'plain_text'}],
                                'type': 'context'},
                                {'block_id': 'TaB',
                                'elements': [{'action_id': 'close',
                                            'text': {'emoji': True,
                                                        'text': '締切',
                                                        'type': 'plain_text'},
                                            'type': 'button',
                                            'value': 'click_me_123'}],
                                'type': 'actions'}],
                    'bot_id': 'B043MPXSR51',
                    'subtype': 'bot_message',
                    'text': "This content can't be displayed.",
                    'ts': '1664764453.264719',
                    'type': 'message'},
        'response_url': 'https://hooks.slack.com/actions/T9R9L3GJ1/4181862974326/KUCw5BBnCRDjaiArAoVaYArl',
        'state': {'values': {}},
        'team': {'domain': 'aprilknights', 'id': 'T9R9L3GJ1'},
        'token': 'nMczOQQ3CWsOlICXSeTNCjXf',
        'trigger_id': '4188477895826.331326118613.d1106a2f654c76eb899123afe7b6091c',
        'type': 'block_actions',
        'user': {'id': 'UAS7W0X6W',
                'name': 'h.kamiyo',
                'team_id': 'T9R9L3GJ1',
                'username': 'h.kamiyo'}}

        try:
            client.conversations_invite(channel=channel_id, users=[test_payload['user']['id']])

        except SlackApiError as e:
            print(e.response["error"])
            if e.response["error"] == "already_in_channel":
                print("このユーザは既にチャンネルに入っています")

        except Exception:
            traceback.print_exc()
