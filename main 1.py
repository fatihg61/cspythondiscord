import bot

if __name__ == '__main__':
    client = bot.run_discord_bot()

    @client.event
    async def on_ready():
        print(f'Staat aan en is actief {client.user}')
        await bot.notify_bot_started()  # Roep de notify_bot_started-functie aan

    client.run()