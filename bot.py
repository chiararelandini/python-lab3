from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
from telegram import ChatAction


#import the list of tasks from the file
from sys import argv
script, file = argv

txt = open(file)
tasks = []
lines = txt.read().split("\n")
txt.close()

for line in lines:
    if line != "":
        tasks.append(line)


def save(tasks):
    target = open(file, "w")
    for task in tasks:
        target.write(task + "\n")
    target.close()

def start(bot, update):
    update.message.reply_text("Hello!")
    print("Hello!")
    commands(bot, update)


def commands(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("1. /showTasks\n" + "2. /newTask <task to add>\n"
    + "3. /removeTask <task to remove>\n" + "4. /removeAllTasks <substring to use to remove all the tasks that contain it>")


def showTasks(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("The tasks you have planned are:")

    if len(tasks) == 0:
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("Nothing to do, here!")
    else:
        tasks.sort()
        for task in tasks:
            bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
            update.message.reply_text(task)

    commands(bot, update)


def newTask(bot, update, args):
    #new = update.message.text
    new = ""
    for task in args:
        new = new + task
    tasks.append(new)
    save(tasks)

    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("The new task was successfully added to the list!")

    commands(bot, update)


def stop(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("Bye bye!")
    save(tasks)
    exit(0);


def error(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("I'm sorry, I can't do that.")
    commands(bot, update)


def main():
    updater = Updater("500897023:AAFgIl4FC5PcsZU-KxZCTpNrx5TULx7xYTU")

    # register a command handler
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("showTasks", showTasks))
    dp.add_handler(CommandHandler("newTask", newTask, pass_args=True))
    dp.add_handler(CommandHandler("stop", stop))    #does not stop the program if /stop from telegram

    # add a non-command handler (messagge handler)
    dp.add_handler(MessageHandler(Filters.text, error))

    updater.start_polling()

    updater.idle()  # handle the stop of the program


if __name__ == "__main__":
    main()