from config.globals import BOT

@BOT.event
async def on_ready():
    print(f"{BOT.user} is ready and online!")