from typing import List

import discord

class reaction_pattern(object):
    def __init__(self, emoji: discord.Emoji, message_patterns: List[str]) -> None:
        self.emoji = emoji
        self.message_patterns = message_patterns

    def __str__(self) -> str: 
        return f'emoji: {self.emoji}, patterns: {self.message_patterns}'
