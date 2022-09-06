import json

def blocks_message(date: str) -> dict:
    text = f"今月の帰社日は{date}になります。\n参加される方は「 *参加* 」のボタンを押してください"

    # BOM有りファイルを読み込む時はutf-8-sigをつけると読み込める
    with open("vote_blocks.json", "r", encoding="utf-8-sig") as jsonf:
        blocks_format = json.load(jsonf)

    blocks_format["blocks"][1]["text"]["text"] = text

    return blocks_format