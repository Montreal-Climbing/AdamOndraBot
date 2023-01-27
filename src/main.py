import reaction
import log

import discord
import os

logger = log.create_logger()

ondra_token = str(os.environ.get('ONDRA_TOKEN'))

intents = discord.Intents.default()
intents.message_content = True

ondra = discord.Client(intents = intents)

logger.info('ADAM IS BORN !!!!!')

# Data stored by adam locally about servers
reaction_db = reaction.load_reactions_db(ondra, logger)

@ondra.event
async def on_ready():
    logger.info(f'We have logged in as {ondra.user}')

@ondra.event
async def on_message(message: discord.Message):
    logger.debug(f'Adam has seen the message \"{message.content}\"')

    await reaction.handle_reaction(message, reaction_db, logger) 

@ondra.event
async def on_guild_emojis_update(guild: discord.Guild, 
                                 before: discord.Sequence[discord.Emoji], 
                                 after: discord.Sequence[discord.Emoji]):
 
    logger.info(f'Emojis on server \"{guild.name}\" were modified. Reloading usable emojis for that server')

    reaction_db[guild] = reaction.load_server_reactions([e for e in after], logger)

ondra.run(token = ondra_token)
