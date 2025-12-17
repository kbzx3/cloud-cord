import discord,os,re
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=keys.env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix="?", intents=discord.Intents.all())
parts = []
files = []
guild_id = #replace with your guild id
@client.command()
async def ping(ctx):    
    latency= round(client.latency*1000)
    await ctx.send(f"Pong! the latnecy of the client is {latency}ms")
def split_file(file_path, ext, chunk_size=8 * 1024 * 1024):
    parts.clear()
    filename = Path(file_path).stem
    with open(file_path, "rb") as f:
        i = 1
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_name = f"{filename}{i}{ext}"
            with open(part_name, "wb") as p:
                p.write(chunk)
            part_filepath = os.path.abspath(part_name)
            parts.append(part_filepath)
            i += 1
    print(parts)
def sanitize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", "-", text)            
    text = re.sub(r"[^a-z0-9_-]", "", text)     
    text = re.sub(r"-{2,}", "-", text)          
    text = re.sub(r"_{2,}", "_", text)          
    text = text.strip("-_")
    return text[:100] or "channel"
async def cli():
    print(f'We have logged in as {client.user}')
    banner = r"""
===========================================================
|    _____ _                 _    _____              _    |
|   / ____| |               | |  / ____|            | |   |
|  | |    | | ___  _   _  __| | | |     ___  _ __ __| |   |
|  | |    | |/ _ \| | | |/ _` | | |    / _ \| '__/ _` |   |
|  | |____| | (_) | |_| | (_| | | |___| (_) | | | (_| |   |
|   \_____|_|\___/ \__,_|\__,_|  \_____\___/|_|  \__,_|   |
===========================================================                                                                                                        
"""
    print("\033[92m" + banner + "\033[0m")
    guild = client.get_guild(guild_id)
    def menu():
        return ("\nMenu:\n 0) Upload file\n 1) Download file\n 2) List channels\n exit) Quit\nChoose: ")
    while True:
        try:
            loop = asyncio.get_running_loop()
            choice = (await loop.run_in_executor(None, input, menu())).strip()

            if choice == '0':
                loop = asyncio.get_running_loop()
                filepath = (await loop.run_in_executor(None, input, "File path: ")).strip()

                if not os.path.isfile(filepath):
                    print("File not found.")
                    continue
                try:
                    split_file(filepath, ext=Path(filepath).suffix)
                    filename_ = sanitize(Path(filepath).stem)
                    names = [c.name for c in guild.text_channels]
                    filename = filename_ + ("-1" if filename_ in names else "")
                    channel = await guild.create_text_channel(filename)
                    for idx, fpath in enumerate(parts, 1):
                        await channel.send(file=discord.File(fpath))
                        print(f"Sent part {idx}/{len(parts)}")
                        os.remove(fpath)
                    print("Upload complete.")
                except Exception as e:
                    print("Upload failed:", e)
                finally:
                    parts.clear()
            elif choice == '1':
                filename_ = (await loop.run_in_executor(
                None, input, "File name (channel): "
                )).strip()

                filename = sanitize(filename_)
                channel = discord.utils.get(guild.text_channels, name=filename)
                if channel is None:
                    print("Channel not found.")
                    continue
                try:
                    messages = [msg async for msg in channel.history(limit=None, oldest_first=True)]
                    if not messages:
                        print("No messages found in channel.")
                        continue
                    for msg in messages:
                        for attachment in sorted(msg.attachments, key=lambda a: a.filename):
                            await attachment.save(attachment.filename)
                            files.append(attachment.filename)
                            print(f"Downloaded {attachment.filename}")
                    out_ext = Path(files[0]).suffix if files else ''
                    with open(filename + "ccd" + out_ext, "ab") as out:
                        for fname in files:
                            with open(fname, "rb") as inf:
                                out.write(inf.read())
                            os.remove(fname)
                    files.clear()
                    print(f"Reconstructed: {filename + 'ccd' + out_ext}")
                except Exception as e:
                    print("Download failed:", e)
                    for f in files:
                        if os.path.exists(f):
                            os.remove(f)
                    files.clear()
            elif choice == '2':
                names = [c.name for c in guild.text_channels]
                print("Channels:")
                for n in names:
                    print(" -", n)
            elif choice == 'exit':
                break
            else:
                print("Invalid choice.")
        except KeyboardInterrupt:
            print("Exiting.")
            break
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    asyncio.create_task(cli())
client.run(DISCORD_TOKEN)
