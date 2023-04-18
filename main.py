import os
import math
import qrcode
import random
import asyncio
import discord
import numpy as np
import matplotlib.pyplot as plt

from replit import db
from datetime import datetime
from keep_alive import keep_alive
from web_scrapping import find_jobs
from mcv_notify import get_notifications
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.environ['TOKEN']

# variable
words    = ['ว่าไง', 'มา', 'เหงา', 'หิว', 'ง่วง', 'โหล', 'เอาเลย', 'ดี']
interact = ['โอ้ววว', 'ไงเงา', 'ฝันดีน้า', 'เยลโล่ว', 'อู้วววววว']

schedule = {
    "monday":    "13.00 - 16.00 PM : [Computer Vision](https://www.mycourseville.com/?q=courseville/course/32214)\n"\
                 "13.00 - 16.00 PM : [Neural Network](https://sites.google.com/view/ssukree/courses/2110571-neural-network-22022?authuser=0)",
    "tuesday":   "08.00 - 09.30 AM : [Software Eng II](https://www.mycourseville.com/?q=courseville/course/32207)\n"\
                 "09.30 - 12.30 AM : [OS Sys Prog](https://www.mycourseville.com/?q=courseville/course/32203)\n"\
                 "13.00 - 16.00 PM : [Data Sci/Eng](https://www.mycourseville.com/?q=courseville/course/32215)",
    "wednesday": "09.00 - 12.00 AM : [Comp Network I](https://www.mycourseville.com/?q=courseville/course/32216)",
    "thursday":  "08.00 - 09.30 AM : [Software Eng II](https://www.mycourseville.com/?q=courseville/course/32207)",
    "friday":    "09.00 - 12.00 AM : [Tech Writing Eng](https://sites.google.com/view/5500308-s12-s2-22/home)"
}

# initial data to replit's database
if "interact" not in db.keys():
    db["interact"] = interact

if "responding" not in db.keys():
    db["responding"] = True


# function to update word in database
def add_words(new_word):
    if "interact" in db.keys():
        interact = db["interact"]
        interact.append(new_word)
        db["interact"] = interact
    else:
        db["interact"] = [new_word]


# function to update word in database
def delete_word(index):
    interact = db["interact"]

    if index.isdigit():
        if len(interact) > index:
            del interact[index]
            db["interact"] = interact

    elif index in interact:
        interact.remove(index)
        db["interact"] = interact


# function to get min/max point
def getMinPoint(data):
    count = 0
    min_data = np.min(data["b"])
    for point in data['b']:
        if point != min_data:
            count += 1
        else:
            break
    return (count, round(min_data))


def getMaxPoint(data):
    count = 0
    max_data = np.max(data["b"])
    for point in data['b']:
        if point != max_data:
            count += 1
        else:
            break
    return (count, round(max_data))


# check if number don't have decimal
def is_integer_num(number):
    if isinstance(number, int):     # 1 = True
        return True
    if isinstance(number, float):   # 1.0 = True
        return number.is_integer()
    return False


# Convert any number (base 10) to any base
def numberToBase(number, base):
    if number == 0:
        return [0]
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
    return digits[::-1]


# convert number from any base to any another base
def numberAnyBase(number, current_base=10, result_base=2):
    base_10 = int(str(number), current_base)
    result = numberToBase(base_10, result_base)
    return "".join(str(number) for number in result)


# to inform me
async def inform():
    await client.wait_until_ready()
    day_of_week = datetime.today().strftime('%A').lower()
    if (day_of_week != "saturday") and (day_of_week != "sunday"):
        embedVar = discord.Embed(
            title="Schedule",
            url="https://docs.google.com/document/d/1C1sF4aS6kFjqWBtU91vSYUvTSxdh9xxXhA9LeUUTbXg/edit#heading=h.8sb6c0hcl62a",
            description=schedule[day_of_week],
            color=discord.Color.blue())
        embedVar.add_field(
            name="Days of week",
            value="For " + datetime.today().strftime('%A') +
            " | [MCV](https://www.mycourseville.com/?q=courseville)" +
            " [Grader](https://nattee.net/grader)",
            inline=False)
        # embedVar.set_author(name="", icon_url="")
        study_room_channel = client.get_channel(808174559529926666)
        Aqioz_id = os.environ['AQIOZ_ID']
        await study_room_channel.send(f"มาเรียนว้อย {Aqioz_id}")
        await study_room_channel.send(embed=embedVar)


# Class Client
class MyClient(discord.Client):

    # introduce yourself
    async def on_ready(self):
        await client.wait_until_ready()
        await client.change_presence(activity=discord.Game(name="$help"))
        print('We have logged in as {0.user}'.format(client))

        # initializing scheduler -> London : timezone="Asia/Bangkok"
        scheduler = AsyncIOScheduler()

        # sends inform at 7 AM (Local Time = London)
        scheduler.add_job(inform, CronTrigger(hour="0", minute="0", second="1"))
        scheduler.start()

    # react to word and command
    async def on_message(self, message):
        global interact
        msg = message.content

        # not reply to itself
        if message.author == client.user:
            return

        # responding
        if db["responding"]:
            option = interact
            if "interact" in db.keys():
                option = option + list(db["interact"])

            if any(word in msg for word in words):
                await message.channel.send(random.choice(option))

        # Detected Word
        if msg.startswith('ไป'):
            await message.reply('ไกปู', mention_author=True)

        if msg.startswith('สีเหลือง'):
            await message.reply('เยลโล่ว!', mention_author=True)

        if msg.lower().startswith('ma'):
            await message.reply('ลุยยยยยยย', mention_author=True)

        if msg.lower().startswith('ฝันดี'):
            await message.reply('ฝันดีคับบบ', mention_author=True)

        if msg.lower().startswith('เนอะ'):
            await message.reply('อื้อ', mention_author=True)

        if 'จิง' in msg:
            await message.channel.send('ฮ้อยย้าา')

        # food menu
        if msg.startswith('กินไร'):
            menu = ["กระเพราหมูสับ", "โจ๊กหมูขอฮาๆ", 'ข้าวไข่เจียว', 'ข้าวไข่ดาว', 'ข้าวไข่ข้น', 'ข้าวไข่ต้ม']
            idx_answer = random.randint(0, len(menu))
            result = menu[idx_answer]
            await message.reply(result, mention_author=True)

        # guessing game
        if msg.startswith('$guess'):
            await message.channel.send('ทายเลขใน 1 ถึง 10 ซิ')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(
                    'ช้าปายย {}.'.format(answer))
            if int(guess.content) == answer:
                await message.channel.send('แม่นน!')
            else:
                await message.channel.send(
                    'ผิด! ตอบ {} โว้ยย'.format(answer))

        # anonymus texting command
        if msg.startswith('$send'):
            channel = msg.split(" ", 2)[1]
            text = msg.split(" ", 2)[2]
            if (channel == "general"):
                general_channel = client.get_channel(694382265081266280)
                await general_channel.send(text)
            elif (channel == "music"):
                music_channel = client.get_channel(791315320648368142)
                await music_channel.send(text)
            elif (channel == "study-room"):
                study_room_channel = client.get_channel(808174559529926666)
                await study_room_channel.send(text)
            elif (channel == "gaming"):
                gaming_chanel = client.get_channel(809839995287633950)
                await gaming_chanel.send(text)
            else:
                test_bot_channel = client.get_channel(928269670635671653)  # test channel
                await test_bot_channel.send(text)

        # add new words
        if msg.startswith('$add'):
            new_word = msg.split("$add", 1)[1]
            add_words(new_word)
            await message.channel.send("เพิ่มละจ้า")

        # delete word in interact
        if msg.startswith("$del"):
            if msg.split("$del", 1)[1] == '':
                interact = list(db["interact"])
                list_of_word = ", ".join(interact)
                await message.channel.send("`" + list_of_word + "`")
                return await message.channel.send(interact)

            interact = []
            if "interact" in db.keys():
                index = int(msg.split("$del", 1)[1])
                delete_word(index)
                interact = list(db["interact"])
                list_of_word = ", ".join(interact)
                await message.channel.send("`" + list_of_word + "`")
            else:
                await message.channel.send("ว่างแย้วครับพี่")

        # list of word
        if msg.startswith('$list'):
            interact = []
            if "interact" in db.keys():
                interact = list(db["interact"])
                list_of_word = ", ".join(interact)
                await message.channel.send("`" + list_of_word + "`")
            else:
                await message.channel.send("ว่างครับพี่")

        # responding command
        if msg.startswith("$responding"):
            value = msg.split("$responding ", 1)[1]

            if value.lower() == "true":
                db["responding"] = True
                await message.channel.send("online now!")
            else:
                db["responding"] = False
                await message.channel.send("offline bye!")

        # Display all commands usage
        if msg.startswith('$help'):
            embed = discord.Embed(
                title="How to use commands",
                url="https://discordpy.readthedocs.io/en/stable/",
                description="use prefix $ | Automatically send schedule at 7 am",
                color=discord.Color.blue()
            )

            command_lists = [
                {'name': '$guess', 'usage': 'Guess number from 1-10\nYou have only 1 guess!'},
                {'name': '$send', 'usage': 'Send anonymous message\n`send [channel] [text]`'},
                {'name': '$responding', 'usage': 'Toggle interact message\n`responding [bool]`'},
                {'name': '$list', 'usage': 'Display all interacting words in database'},
                {'name': '$add', 'usage': 'Add word \n`add [word]`'},
                {'name': '$del', 'usage': 'Delete word\n`del [index / word]`'},
                {'name': '$random', 'usage': 'Random from list\n`random [list]`'},
                {'name': '$qrcode', 'usage': 'Create QR-Code\n`qrcode [data / link]`'},
                {'name': '$poll', 'usage': 'Create poll with reaction\n`poll [title] [list]`'},
                {'name': '$code', 'usage': 'Create codeblock\n`code [language]`'},
                {'name': '$cal', 'usage': 'Act as a calculator\nType `บาย` to quit'},
                {'name': '$base', 'usage': 'Convert number base\n`base [number] [old_base] [new_base]`'},
                {'name': '$master1', 'usage': 'Master Theorem for dividing function\n`master1 [a] [b] [d]`'},
                {'name': '$master2', 'usage': 'Master Theorem for decrease function\n`master2 [a] [b] [k]`'},
                {'name': '$plot', 'usage': 'Plot random points with various size\n`plot [number]`'},
                {'name': '$inform', 'usage': 'Inform current `author`\'s schedule'},
                {'name': '$job', 'usage': 'Filter jobs from website\n`job [keyword] [filter]`'},
                {'name': '$noti', 'usage': 'Notification from MCV\n`noti [days] [type]`'},
            ]

            # embed.set_thumbnail(url="https://i.pinimg.com/originals/13/8d/52/138d52a8f429510e2c16bd67990dae3c.jpg")
            for command in command_lists:
                embed.add_field(
                    name=command['name'],
                    value=command['usage'],
                    inline=True
                )

            # embed.set_author(name="Aqioz")
            Aqioz_id = os.environ['AQIOZ_ID']
            embed.add_field(name="__**Author**__", value=f"> {Aqioz_id}\n> Bhuribhat@gmail.com", inline=False)
            await message.channel.send(embed=embed)

        # calculator command
        if msg.startswith("$cal"):
            await message.channel.send('ก็มาดิ')
            try:
                equation = await self.wait_for('message', timeout=10.0)
                if equation.content == "บาย":
                    await message.channel.send("บายน้า")
            except asyncio.TimeoutError:
                return await message.channel.send('ไปละปวดหมอง')
            while equation.content != "บาย":
                answer = "ตอบ " + str(eval(equation.content))
                await message.channel.send(answer)
                try:
                    equation = await self.wait_for('message', timeout=10.0)
                    if equation.content == "บาย":
                        await message.channel.send("บายน้า")
                except asyncio.TimeoutError:
                    return await message.channel.send('ไปละปวดหมอง')

        # coding template
        if msg.startswith("$code"):
            language = msg.split("$code ", 1)[1]
            embedVar = discord.Embed(title="Coding Template",
                                     description=f"` ```{language}\n`\t `\n``` `",
                                     color=0x00ff00)
            embedVar.add_field(name="Description",
                               value=f"Template for {language} language",
                               inline=False)
            study_room_channel = client.get_channel(808174559529926666)
            await study_room_channel.send(embed=embedVar)

        # random list of thing split by comma (",")
        if msg.startswith("$random"):
            list_thing = msg.split("$random", 1)[1].split(",")
            if (list_thing == ['']):
                result = "overflow"
                value = "None"
            else:
                result = random.choice(list_thing)
                value = ", ".join(list_thing)
            embedVar = discord.Embed(title="Result", description=f"`{result.strip()}`", color=0xe91e63)
            embedVar.add_field(name="Randoming from", value=value, inline=False)
            await message.channel.send(embed=embedVar)

        # calculate time complex using master theorem divide function
        if msg.startswith("$master1"):
            coef = msg.split("$master1", 1)[1].split()
            if (len(coef) == 0):
                await message.channel.send("__**usage**__: `$master1 a b d`")
                result = "Big Thetha"
                value = "`T(n) = aT(n/b) + Θ(n^d)`\n\n__**Conditions**__:\na >= 1, b > 1, c = log_b(a), d >= 0, T(0) = 1"
            else:
                if (len(coef) > 3):
                    await message.channel.send("*Invalid Input..*")
                    return
                a, b, d = [int(num) for num in coef]
                if a < 1 or b <= 1 or d < 0:
                    await message.channel.send("*Invalid Input..*")
                    return
                c = math.log(a, b)

                # convert to integer if not decimal
                if is_integer_num(a):
                    a = math.ceil(a)
                else:
                    a = round(a, 2)
                if is_integer_num(b):
                    b = math.ceil(b)
                else:
                    b = round(b, 2)
                if is_integer_num(c):
                    c = math.ceil(c)
                else:
                    c = round(c, 2)
                if is_integer_num(d):
                    d = math.ceil(d)
                else:
                    d = round(d, 2)
                str_c = f"log_{b}({a})"

                if a == 1:
                    a = ''
                if d == 0:
                    value = f" T(n) = {a}T(n/{b}) + 1"
                elif d == 1:
                    value = f"T(n) = {a}T(n/{b}) + Θ(n)"
                else:
                    value = f"T(n) = {a}T(n/{b}) + Θ(n^{d})"
                if d < c:
                    await message.channel.send("Master theorem case 1 : d < c")
                    if not is_integer_num(c):
                        result = f"Θ(n^{str_c}) = Θ(n^{c})"
                    else:
                        if c == 1:
                            result = "Θ(n)"
                        else:
                            result = f"Θ(n^{c})"
                elif d == c:
                    await message.channel.send("Master theorem case 2 : d = c")
                    if not is_integer_num(c):
                        result = f"Θ(n^{str_c}log(n)) = Θ(n^{str_c}log(n))"
                    else:
                        if c == 0:
                            result = "Θ(log(n)"
                        elif c == 1:
                            result = "Θ(nlog(n)"
                        else:
                            result = f"Θ(n^{c}log(n)"
                elif d > c:
                    await message.channel.send("Master theorem case 3 : d > c")
                    if d == 1:
                        result = "Θ(n)"
                    else:
                        result = f"Θ(n^{d})"
            embedVar = discord.Embed(title="Divide Function", description=value, color=0xd69f09)
            embedVar.add_field(name="Time Complexity", value=f"||`{result.strip()}`||", inline=False)
            await message.channel.send(embed=embedVar)

        # calculate time complex using master theorem decreasing function
        if msg.startswith("$master2"):
            coef = msg.split("$master2", 1)[1].split()
            if (len(coef) == 0):
                await message.channel.send("__**usage**__: `$master2 a b k`")
                result = "Big Oh Notation"
                value = "`T(n) = aT(n - b) + O(n^k)`\n\n__**Conditions**__:\na >= 1, b > 0, k >= 0, T(0) = 1"
            else:
                if (len(coef) > 3):
                    await message.channel.send("*Invalid Input..*")
                    return
                a, b, k = [int(num) for num in coef]
                if a < 1 or b <= 0 or k < 0:
                    await message.channel.send("*Invalid Input..*")
                    return

                # convert to integer if it has no decimal, 2 precision otherwise
                if is_integer_num(a):
                    a = math.ceil(a)
                else:
                    a = round(a, 2)
                if is_integer_num(b):
                    b = math.ceil(b)
                else:
                    b = round(b, 2)
                if is_integer_num(k):
                    k = math.ceil(k)
                else:
                    k = round(k, 2)

                if a == 1:
                    a = ''
                if k == 0:
                    value = f" T(n) = {a}T(n - {b}) + 1"
                elif k == 1:
                    value = f" T(n) = {a}T(n - {b}) + O(n)"
                else:
                    value = f" T(n) = {a}T(n - {b}) + O(n^{k})"
                a = 1 if a == '' else a

                if a == 1:
                    await message.channel.send("Master theorem case 1 : a = 1")
                    if k + 1 > 1:
                        result = f"O(n^{k + 1})"
                    else:
                        result = f"O(n)"

                elif a > 1:
                    await message.channel.send("Master theorem case 2 : a > 1")
                    if k > 0:
                        if k == 1:
                            k = "O(n"
                        else:
                            k = f"O(n^{k}"
                        if b > 1:
                            result = f"{k} * {a}^(n/{b}))"
                        else:
                            result = f"{k} * {a}^n)"
                    else:
                        if b > 1:
                            result = f"O({a}^(n/{b}))"
                        else:
                            result = f"O({a}^n)"

            embedVar = discord.Embed(title="Decrease Function", description=value, color=0xd69f09)
            embedVar.add_field(name="Time Complexity", value=f"||`{result.strip()}`||", inline=False)
            await message.channel.send(embed=embedVar)

        # inform
        if msg.startswith("$inform"):
            day_of_week = datetime.today().strftime('%A').lower()
            if (day_of_week != "saturday") and (day_of_week != "sunday"):
                embedVar = discord.Embed(
                    title="Schedule",
                    url="https://docs.google.com/document/d/1C1sF4aS6kFjqWBtU91vSYUvTSxdh9xxXhA9LeUUTbXg/edit#heading=h.8sb6c0hcl62a",
                    description=schedule[day_of_week],
                    color=discord.Color.blue())
                embedVar.add_field(
                    name="Days of week",
                    value="For " + datetime.today().strftime('%A') +
                    " | [MCV](https://www.mycourseville.com/?q=courseville)" +
                    " [Grader](https://nattee.net/grader)",
                    inline=False)
            await message.channel.send(embed=embedVar)

        # plot graph within 10,000 number
        if msg.startswith("$plot"):
            number = int(msg.split("$plot ", 1)[1])
            if (number >= 1000):
                await message.channel.send("too much bro")
            else:
                data = {
                    'a': np.arange(number),
                    'c': np.random.randint(0, number, number),
                    'd': np.random.randn(number)
                }
                data['b'] = data['a'] + 10 * np.random.randn(number)
                data['d'] = np.abs(data['d']) * 100

                # Set background color and axis
                plt.figure(figsize=(10, 6), facecolor="#303340")
                ax = plt.axes()
                ax.set_facecolor("#303340")
                ax.tick_params(axis="x", color="white")
                ax.tick_params(axis="y", color="white")
                plt.xticks(color="white")
                plt.yticks(color="white")

                # plot
                plt.scatter('a', 'b', c='c', s='d', data=data)
                plt.xlabel('Data', color="cyan")
                plt.ylabel('Value', color="cyan")
                plt.title(r'$\Sigma=$' + str(number), color="orange")

                await message.channel.send(f"min data = {getMinPoint(data)}")
                await message.channel.send(f"max data = {getMaxPoint(data)}")

                # send graph to channel
                plt.savefig('.\\assets\\graph.png', bbox_inches='tight')
                await message.channel.send(file=discord.File('.\\assets\\graph.png'))

        # QR-Code PNG
        if msg.startswith("$qrcode"):
            QR = qrcode.QRCode(version=1, box_size=10, border=2)
            data = msg.split("$qrcode ", 1)[1]
            QR.add_data(data)
            QR.make(fit=True)

            # fill_color='black', back_color='white'
            img = QR.make_image()
            img.save('.\\assets\\QRCode.png')

            # send picture to channel
            await message.channel.send(file=discord.File('.\\assets\\QRCode.png'))

        if msg.startswith("$base"):
            attr = msg.split("$base", 1)[1].split()
            if (len(attr) == 0):
                await message.channel.send("__**usage**__: `$base number base convert_base`")
                result = "Number in base X"
                value = "base >= 2"
                base = 'n'
                convert_base = 'x'
            else:
                if (len(attr) > 3):
                    await message.channel.send("*Invalid Input..*")
                    return
                number, base, convert_base = [int(num) for num in attr]
                result = numberAnyBase(number, base, convert_base)
                value = number

            embedVar = discord.Embed(title="From base " + str(base), description=value, color=0xa84300)
            embedVar.add_field(name="Convert to base " + str(convert_base), value=f"||`{result.strip()}`||", inline=False)
            await message.channel.send(embed=embedVar)

        # jobs seeker with csv file
        if msg.startswith("$job"):
            attr = msg.split("$job", 1)[1].split()
            if (len(attr) == 0):
                await message.channel.send("__**usage**__: `$job keyword unwanted_skill`")
                return
            else:
                if (len(attr) > 2):
                    await message.channel.send("*Invalid Input..*")
                    return

                keyword, unwant_skill = attr
                df = find_jobs(keyword, unwant_skill)
                df = df.drop(['Job Description', 'More Information', 'Skills Required'], axis=1)
                
                length = df.shape[0]
                df = df.head(5).to_string()

            embedVar = discord.Embed(title=f"All Jobs with {keyword} skill", description=f"filter out {unwant_skill}", color=0xa84300)
            embedVar.add_field(name=f"Found {length} jobs", value=f"```{df}```", inline=False)
            await message.channel.send(embed=embedVar)
            await message.channel.send("for more detail please check `csv file`")
            await message.channel.send(file=discord.File(".\\assets\\jobs.csv"))

        # poll with reactions
        if msg.startswith("$poll"):
            emoji = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
            choices = msg.split("$poll")[1].split()
            if (len(choices) == 0):
                await message.channel.send("__**usage**__: `$poll title <list of choice>`")
                return
            if (len(choices) > len(emoji) + 1):
                await message.channel.send("too much bro")
                return

            title = choices[0]
            display_choices = ''
            for i in range(len(choices[1:])):
                display_choices += f"{emoji[i]} {choices[1:][i]}\n"
            embedVar = discord.Embed(title=f"Please vote!", color=0x64395d)
            embedVar.add_field(name=title, value=f"```{display_choices}```", inline=False)
            pollmsg = await message.channel.send(embed=embedVar)

            for i in range(len(choices[1:])):
                await pollmsg.add_reaction(emoji[i])

        # get mcv notifications within 1 week
        if msg.startswith("$noti"):
            attr = msg.split("$noti")[1].split()
            if len(attr) > 2:
                await message.channel.send("__**usage**__: `$noti days type`")
                await message.channel.send("type must be between `Assignment, Material, Announcement`")
                return

            if len(attr) == 0:
                notifications = get_notifications()
            elif len(attr) == 1:
                if attr[0].isnumeric():
                    notifications = get_notifications(days=attr[0])
                elif attr[0].title() in ['Assignment', 'Material', 'Announcement']:
                    notifications = get_notifications(select=attr[0])
                else:
                    await message.channel.send("type must be between `Assignment, Material, Announcement`")
                    return
            else:
                notifications = get_notifications(attr[0], attr[1])

            embedVar = discord.Embed(title="MCV Notification", color=discord.Color.blue())
            for notification in notifications:
                value = f"```{notification[1]}```{notification[2]}"
                embedVar.add_field(name=notification[0], value=value, inline=False)
            await message.channel.send(embed=embedVar)


# driver
client = MyClient()
keep_alive()
client.run(TOKEN)
