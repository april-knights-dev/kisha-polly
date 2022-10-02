import unittest
import json

from app.blocks import BlocksChangeMessage


class TestBlocks(unittest.TestCase):

    def test_change_blocks(self):
        date_text = "12/25"
        channel_id = "AAAAA9"

        with open("tests/test_vote_blocks.json", "r", encoding="utf-8-sig") as jsonf:
            result_blocks_format = json.load(jsonf)

        blockschange = BlocksChangeMessage()
        
        blockschange.blocks_change_date(date_text)
        blockschange.blocks_add_channelid(channel_id)

        self.assertEqual(result_blocks_format, blockschange.blocks_format)
