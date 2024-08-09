from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

tasks = {}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id not in tasks:
        tasks[user_id] = []
    update.message.reply_text('Добро пожаловать!\n'
                               '\n\n Для получения информации введите /help')

def add(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    task = ' '.join(context.args)
    if task:
        tasks[user_id].append(task)
        update.message.reply_text(f'Задача "{task}" добавлена.')
    else:
        update.message.reply_text('Пожалуйста, укажите название задачи.')

def list(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if tasks[user_id]:
        task_list = '\n'.join([f'{i+1}. {task}' for i, task in enumerate(tasks[user_id])])
        update.message.reply_text(f'Ваши задачи:\n{task_list}')
    else:
        update.message.reply_text('У вас нет задач.')

def delete(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    try:
        task_index = int(context.args[0]) - 1
        removed_task = tasks[user_id].pop(task_index)
        update.message.reply_text(f'Задача "{removed_task}" удалена.')
    except (IndexError, ValueError):
        update.message.reply_text('Пожалуйста, укажите правильный номер задачи.')

def edit(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    try:
        task_index = int(context.args[0]) - 1
        new_task = ' '.join(context.args[1:])
        tasks[user_id][task_index] = new_task
        update.message.reply_text(f'Задача обновлена на "{new_task}".')
    except (IndexError, ValueError):
        update.message.reply_text('Пожалуйста, укажите правильный номер задачи и новое название.')

def help(update: Update, context: CallbackContext) -> None:
    help_text = (
        "/start - Начать взаимодействие с ботом\n"
        "/add <название задачи> - Добавить новую задачу\n"
        "/list - Просмотреть все задачи\n"
        "/delete <номер задачи> - Удалить задачу\n"
        "/edit <номер задачи> <новое название> - Редактировать задачу\n"
        "/help - Показать список команд"
    )
    update.message.reply_text(help_text)

def main() -> None:
    updater = Updater("7380800891:AAE9okJyeQ-44fiO3atlO7QmSUjYqpPydQ0")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("list", list))
    dispatcher.add_handler(CommandHandler("delete", delete))
    dispatcher.add_handler(CommandHandler("edit", edit))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
