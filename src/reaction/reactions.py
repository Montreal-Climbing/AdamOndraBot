import json
import logging
import os
import re

import discord

from reaction.reaction_pattern import reaction_pattern

"""
TODO: Keep a dictionary that matches each guild with it's usable reactions.
TODO: Update the dictionary routinely when the "reactions.json" file is modified
"""


reaction_filepath = os.getcwd() + '/resources/reactions.json'

def load_reactions_from_file(logger: logging.Logger):
    """
    load_reactions_from_file loads the `reactions.json` file located in the resources
    folder

    Parameters: 
        logger - 

    Returns: 
        
    """

    with open(reaction_filepath, 'r') as file:
        reaction_json = json.load(file)
   
    logger.debug('The list of available reactions to use has been loaded')
    
    return reaction_json['reactions']

def is_pattern_in_message(pattern: str, message: discord.Message) -> bool:
    """
    Performs a regex match to find a pattern within a specific discord message. 

    Parameters: 
        pattern: The pattern the match for in the user message.
        message: The message written by a discord user.

    Returns:
        bool: True if the pattern is found in the message, otherwise False.
    """
    return bool(re.match(pattern=pattern, string=message.content.lower()))

def does_message_contain_patterns(patterns: list[str], message: discord.Message) -> bool:
    """
    Performs regex matches on an input list of patterns against a specific discord message.

    Parameters:
        patterns: The list of pattern to match for in the user message.
        message: The message written by a discord user.

    Returns:
        bool: True if one of the patterns is present in the discord message, otherwise False.
    """
    for pattern in patterns:
        if is_pattern_in_message(pattern, message):
            return True

    return False

async def handle_reaction(message: discord.Message, 
                          reactions_db: dict[discord.Guild, list[reaction_pattern]], 
                          logger: logging.Logger):

    if reactions_db is None or message.guild is None:
        return

    usable_reactions = reactions_db.get(message.guild)

    print(usable_reactions)

    if usable_reactions is None:
        return

    for r in usable_reactions:
        logger.debug(f'Adam is looking if he can react to message \"{message.content}\" with {r.emoji}')

        if does_message_contain_patterns(r.message_patterns, message):
            logger.debug(f'Adam reacted to message \"{message.content}\" with {r.emoji}')
            await message.add_reaction(r.emoji) 

def __get_usable_reactions__(emojis: list[discord.Emoji], reactions) -> list[reaction_pattern]:
    usable_reactions = []
    for e in emojis:
        for r in reactions:
            if e.name == r["emoji"]:
                usable_reactions.append(reaction_pattern(e, r["message_patterns"]))

    return usable_reactions

def load_reactions_db(ondra: discord.Client, logger: logging.Logger) -> dict[discord.Guild, list[reaction_pattern]]:
    db = {}
    reactions = load_reactions_from_file(logger=logger)

    for guild in ondra.guilds:
        logger.debug(f'Adam is loading the usable reactions for the \"{guild.name}\" discord server')

        # Convert the weird tuple into a list of emojis
        emojis = [e for e in guild.emojis]

        db[guild] = __get_usable_reactions__(emojis, reactions)

    logger.debug('Adam has created his reaction database')

    return db

def load_server_reactions(emojis: list[discord.Emoji], logger: logging.Logger) -> list[reaction_pattern]:  
    return __get_usable_reactions__(emojis, load_reactions_from_file(logger=logger))




    
