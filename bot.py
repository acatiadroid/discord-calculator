import discord
from discord.ext import commands


class CalculatorBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="calc ",
            case_insensitive=True
        )

    async def on_ready(self):
        print("Hey there")


bot = CalculatorBot()


@bot.command(name='init', aliases=['new'])
async def initialize(ctx):
    class InteractiveCalculatorView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.timeout = 300
            self.to_calc = []
            self.answer = None
            self.ctx = ctx
            self.msg = None
            self.disable_toggle = False

        async def on_timeout(self) -> None:
            for item in self.children:
                item.disabled = True

        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if self.ctx.author.id != interaction.user.id:
                await interaction.response.send_message("This isn't yours to control.", ephemeral=True)
                return False
            else:
                return True

        @discord.ui.button(style=discord.ButtonStyle.grey, label='7', row=1)
        async def btn_seven(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(7)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.grey, label='8', row=1)
        async def btn_eight(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(8)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.grey, label='9', row=1)
        async def btn_nine(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(9)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label=' + ', row=1)
        async def btn_add(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append("+")
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.red, label='Clear', row=1)
        async def btn_clear(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.clear()
            await self.msg.edit(embed=self.consistent_embed(self.ctx, f"Output shown here"))

        @discord.ui.button(style=discord.ButtonStyle.grey, label='4', row=2)
        async def btn_four(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(4)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.grey, label='5', row=2)
        async def btn_five(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(5)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.grey, label='6', row=2)
        async def btn_six(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(6)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label=' - ', row=2)
        async def btn_minus(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append("-")
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.red, label='Kill', row=2)
        async def btn_kill(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.clear()
            await self.msg.edit(content='This calculator has been disabled.', embed=None)
            for item in self.children:
                item.disabled = True
            self.stop()
            self.disable_toggle = True

        @discord.ui.button(style=discord.ButtonStyle.grey, label='1', row=3)
        async def btn_one(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(1)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.grey, label='2', row=3)
        async def btn_two(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(2)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.grey, label='3', row=3)
        async def btn_three(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(3)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label=' ÷ ', row=3)
        async def btn_divide(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append("/")
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label=' . ', row=3)
        async def btn_decimal(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(".")
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.grey, label=' 0 ', row=4)
        async def btn_zero(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(0)
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label=' ( ', row=4)
        async def btn_openbracket(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append("(")
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label=' ) ', row=4)
        async def btn_closedbracket(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append(")")
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label=' × ', row=4)
        async def btn_multiply(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.to_calc.append("*")
            await self.update_content()

        @discord.ui.button(style=discord.ButtonStyle.green, label=' = ', row=4)
        async def btn_enter(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.enter()

        def consistent_embed(self, context: commands.Context, content: str):
            embed = discord.Embed(
                description=f"```yaml\n{content}```",
                color=discord.Colour.blurple()
            )
            embed.set_author(name=context.author, icon_url=context.author.avatar.url)

            return embed

        async def enter(self):
            to_calc = "".join(str(x) for x in self.to_calc)
            try:
                ans = eval(to_calc)
                self.answer = "{:,}".format(ans)
            except ZeroDivisionError:
                self.answer = "❎ Cannot divide by zero"
            except SyntaxError:
                self.answer = "❎ Syntax Error"
            except Exception:
                self.answer = "❎ Error"

            await self.msg.edit(embed=self.consistent_embed(self.ctx, f"{to_calc} = {self.answer}"))

        async def update_content(self):
            to_calc = "".join(str(x) for x in self.to_calc)
            return await self.msg.edit(embed=self.consistent_embed(self.ctx, to_calc))

    msg = await ctx.send("Loading calculator...")
    view = InteractiveCalculatorView()
    view.msg = msg
    embed = discord.Embed(
        description=f"```yaml\nOutput shown here```",
        color=discord.Colour.blurple()
    )
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

    await msg.edit(embed=embed, view=view, content=None)

    await view.wait()
    if view.disable_toggle:
        await msg.edit(view=view)


if __name__ == "__main__":
    bot.run("")
