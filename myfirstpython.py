import telebot
import codeforces_api
import datetime

bot = telebot.TeleBot(token="5675536797:AAFu9OcFOFs9eidnyIemRQRjSTu5Syo0RPo")
code = codeforces_api.CodeforcesApi()


@bot.message_handler(commands=["contest"])
def temp(message):
    msg = code.contest_list(gym=False)
    msg = sorted(msg, key=lambda x: x.start_time_seconds)
    for x in msg:
        if (x.relative_time_seconds < 0):
            curr = f" Name: {x.name} \nDatetime: {datetime.datetime.fromtimestamp(x.start_time_seconds).strftime('%d-%m-%Y %H:%M:%S')} \nTime Remaining : {datetime.timedelta(seconds=abs(x.relative_time_seconds))} \nDuration: {x.duration_seconds/3600} hours \nRegistration link: https://codeforces.com/contestRegistration/{x.id} \nContest Link: https://codeforces.com/contest/{x.id}"
            bot.send_message(message.chat.id, curr)


@bot.message_handler(commands=["userrating"])
def temp(message):
    bot.send_message(message.chat.id, "Send me Handle:")
    bot.register_next_step_handler(message, getuserinfo)


def getuserinfo(message):
    try:
        user = code.user_info(handles=[message.text])
    except:
        bot.send_message(message.chat.id, "username is invalid")
    else:
        curr = f"Name : {user[0].first_name} {user[0].last_name}\nCurrent Rating: {user[0].rank} ({user[0].rating})\nMax Rating: {user[0].max_rank} ({user[0].max_rating})\nOrganization: {user[0].organization}\nLocation: {user[0].city},{user[0].country}\nAvatar: {user[0].avatar} \nLink: https://codeforces.com/profile/{message.text}"
        bot.send_message(message.chat.id, curr)


bot.polling()
