from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter

if __name__ == "__main__":
    print("Bot started!")
    set_default_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()
