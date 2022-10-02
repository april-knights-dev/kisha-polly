import json
import logging

logging.basicConfig(level=logging.INFO)


class BlocksChangeMessage:

    def __init__(self) -> None:
        try:
            # BOM有りファイルを読み込む時はutf-8-sigをつけると読み込める
            with open("vote_blocks.json", "r", encoding="utf-8-sig") as jsonf:
                self.blocks_format = json.load(jsonf)
        except FileNotFoundError:
            logging.error("vote_blocks.jsonが見つかりませんでした")

    def blocks_change_date(self, date: str) -> dict:
        text = f"次回の帰社日は{date}になります。\n参加される方は「 *参加* 」のボタンを押してください"
        self.blocks_format["blocks"][1]["text"]["text"] = text

    def blocks_add_channelid(self, channel_id: str) -> dict:
        self.blocks_format["blocks"][4]["elements"][0]["text"] = channel_id
