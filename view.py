import discord
import asyncio
from mcv_notify import get_notifications


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


class NotiMenu(discord.ui.View):

    # the decorator that lets you specify the properties of the select menu
    @discord.ui.select(

        # the placeholder text that will be displayed if nothing is selected
        placeholder="Choose a filters!",

        min_values=1,  # the minimum number of values that must be selected by the users
        max_values=2,  # the maximum number of values that can be selected by the users

        options=[

            # Filter by Type
            discord.SelectOption(
                emoji="📢",
                label="Announcement",
                description="Pick Type Announcement!"
            ),
            discord.SelectOption(
                emoji="📝",
                label="Assignment",
                description="Pick Type Assignment!"
            ),
            discord.SelectOption(
                emoji="📚",
                label="Material",
                description="Pick Type Material!"
            ),

            # Filter by days
            discord.SelectOption(
                emoji="0️⃣",
                label="0 Days",
                value="0",
                description="Within today!"
            ),
            discord.SelectOption(
                emoji="1️⃣",
                label="1 Days",
                value="1",
                description="Within 1 day!"
            ),
            discord.SelectOption(
                emoji="2️⃣",
                label="2 Days",
                value="2",
                description="Within 2 days!"
            ),
            discord.SelectOption(
                emoji="3️⃣",
                label="3 Days",
                value="3",
                description="Within 3 days!"
            ),
            discord.SelectOption(
                emoji="4️⃣",
                label="4 Days",
                value="4",
                description="Within 4 days!"
            ),
            discord.SelectOption(
                emoji="5️⃣",
                label="5 Days",
                value="5",
                description="Within 5 days!"
            ),
            discord.SelectOption(
                emoji="6️⃣",
                label="6 Days",
                value="6",
                description="Within 6 days!"
            ),
            discord.SelectOption(
                emoji="7️⃣",
                label="7 Days",
                value="7",
                description="Within 7 days!"
            ),
        ]
    )

    # the function called when the user is done selecting options
    async def select_callback(self, interaction, select):
        await interaction.response.defer()
        await asyncio.sleep(10)

        if len(select.values) == 1:
            if select.values[0].isnumeric():
                notifications = get_notifications(days=select.values[0])
            elif select.values[0].title() in ['Assignment', 'Material', 'Announcement']:
                notifications = get_notifications(select=select.values[0])
        if len(select.values) == 2:
            filter, days = select.values
            print(f"filter = {filter}, days = {days}")
            notifications = get_notifications(days=days, select=filter)

        embedVar = discord.Embed(title="MCV Notification", color=discord.Color.blue())
        for notification in notifications:
            value = f"```{notification[1]}```{notification[2]}"
            embedVar.add_field(name=notification[0], value=value, inline=False)
            
        await interaction.followup.send(embed=embedVar)
