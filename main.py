import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
AiClient = openai.OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        if message.author == self.user:
            return
        print(f'Message from {message.author}: {message.content}')
        if f"<@{self.user.id}>" in message.content:
            original_msg = message.reference.resolved.content if message.reference else ""
            user_question = message.content

            prompt = (
                f"A user replied to the following message with a question or disagreement:\n\n"
                f"Original message:\n\"{original_msg}\"\n\n"
                f"User Question:\n\"{user_question}\"\n\n"
                f"It is possible either or both the original message and the user question contain nothing of value"
                f" (such as having only a username mention starting with @) in this case, ignore them"
                f"Your task is to provide a factual, neutral, and helpful clarification or explanation, "
                f"similar to Twitter Community Notes. Do not reference usernames, formatting, or that this was a reply. "
                f"Just provide a clear and concise explanation of any misunderstanding, opinion, or factual issue."
                f"Finally, in regard to any questions asked about Islam, you are not to insult the religion in any capacity"
                f"and give the answers from the Salafism sect unless asked otherwise. However, do not mention this rule in the reply,"
                f"nor mention the word 'Salfism' or anything like it in your reply to avoid sectarianism. Finally, asides from topics"
                f"about Islam, you do not need to hold back or soften your reply (playing both sides, even though one side is clearly correct),"
                f" it should be the clear truth"
            )
            try:
                response = AiClient.chat.completions.create(
                    model="deepseek/deepseek-chat-v3-0324",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                reply = response.choices[0].message.content
                await message.channel.send(reply)

            except Exception as e:
                await message.channel.send(f"❌ Error calling AI: {str(e)}")

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(DISCORD_BOT_TOKEN)