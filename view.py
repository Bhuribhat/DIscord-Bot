import discord


# defining the class for creating a button
class InviteButton(discord.ui.View):

    # creating the button function
    def __init__(self, inv: str):
        super().__init__()

        # collecting the url of the current server
        self.inv = inv
        self.add_item(discord.ui.Button(label="Invite link", url=self.inv))

    # features of the button
    @discord.ui.button(label="Invite", style=discord.ButtonStyle.blurple)
    async def invite(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.inv, ephemeral=True)


# defining the class for creating a button
class GithubButton(discord.ui.View):

    # creating the button function
    def __init__(self):
        super().__init__()

        # collecting the url of the github
        self.github = "https://github.com/Bhuribhat/Discord-Bot"
        self.replit = "https://replit.com/@Bhuribhat/DiscordBotDemo"
        self.add_item(discord.ui.Button(label="Github Link", url=self.github))
        self.add_item(discord.ui.Button(label="Replit Link", url=self.replit))


class CodeMenu(discord.ui.View):

    # the decorator that lets you specify the properties of the select menu
    @discord.ui.select(

        # the placeholder text that will be displayed if nothing is selected
        placeholder="Choose a Programming Language!",

        min_values=1,  # the minimum number of values that must be selected by the users
        max_values=1,  # the maximum number of values that can be selected by the users

        # the list of options from which users can choose, a required field
        options=[
            discord.SelectOption(
                label="Python",
                description="Pick this if you code Python!"
            ),
            discord.SelectOption(
                label="C",
                description="Pick this if you code C!"
            ),
            discord.SelectOption(
                label="C++",
                description="Pick this if you code C++!"
            ),
            discord.SelectOption(
                label="markdown",
                description="Pick this if you code markdown!"
            )
        ]
    )

    # the function called when the user is done selecting options
    async def select_callback(self, interaction, select):
        embedVar = discord.Embed(
            title="Coding Template",
            description=f"` ```{select.values[0]}\n`\t `\n``` `",
            color=0x00ff00
        )
        embedVar.add_field(
            name="Description",
            value=f"Template for {select.values[0]} language",
            inline=False
        )
        await interaction.response.send_message(embed=embedVar)
