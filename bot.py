import asyncio
import discord
import os
from discord.ext import commands
from config import TOKEN_BOT, DISCORD_CHANNEL_ID, WATCH_FOLDER

QUEUE_FILE = "queue.txt"

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)

class AnalyzeButton(discord.ui.View):
    def __init__(self, filename):
        super().__init__(timeout=600)
        self.filename = filename

    @discord.ui.button(label="Analisar Vídeo", style=discord.ButtonStyle.primary, emoji="▶️")
    async def analyze(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        button.label = "Processando..."
        button.style = discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)
        
        await interaction.followup.send(f"⚙️ Iniciando análise de `{self.filename}`...", ephemeral=True)

        try:
            full_video_path = os.path.join(WATCH_FOLDER, self.filename)

            process = await asyncio.create_subprocess_exec(
                "python", "analyzer.py", full_video_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            output = stdout.decode('utf-8', errors='replace').strip()
            err_details = stderr.decode('utf-8', errors='replace').strip()
            
            if process.returncode == 0:
                resumo = output.split("RESULTADOS DA AVALIACAO")[-1] if "RESULTADOS DA AVALIACAO" in output else "Concluído."
                
                embed = discord.Embed(
                    title="✅ Análise Concluída",
                    description=f"Arquivo: `{self.filename}`",
                    color=discord.Color.green()
                )
                embed.add_field(name="Resultados", value=f"```\n📌 RESULTADOS{resumo}\n```")
                
                await interaction.channel.send(embed=embed)
            else:
                await interaction.followup.send(f"❌ Erro no script:\n```\n{err_details[:500]}\n```", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"❌ Erro ao disparar análise: {str(e)}", ephemeral=True)

async def check_queue():
    await bot.wait_until_ready()
    channel = await bot.fetch_channel(DISCORD_CHANNEL_ID)

    while not bot.is_closed():
        if os.path.exists(QUEUE_FILE):
            try:
                with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                if lines:
                    filename = lines[0].strip()
                    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
                        f.writelines(lines[1:])

                    embed = discord.Embed(
                        title="📹 Novo Vídeo na Fila",
                        description=f"Um novo arquivo foi detectado.\n\n**Arquivo:** `{filename}`",
                        color=discord.Color.blue()
                    )
                    await channel.send(embed=embed, view=AnalyzeButton(filename))
            except Exception as e:
                print(f"Erro ao ler fila: {e}")

        await asyncio.sleep(2)

@bot.event
async def on_ready():
    print(f"🤖 Bot online: {bot.user}")
    if not hasattr(bot, 'queue_task'):
        bot.queue_task = bot.loop.create_task(check_queue())

bot.run(TOKEN_BOT)