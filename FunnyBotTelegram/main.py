import random
import telebot
import requests
from bs4 import BeautifulSoup

# In the brackets should be your bot token api
# For example '123' or '2F6!&3g'
bot = telebot.TeleBot('')

image_request_users = []
dice_values_dict = {1: "\U00000031\U000020E3", 2: "\U00000032\U000020E3",
                    3: "\U00000033\U000020E3", 4: "\U00000034\U000020E3",
                    5: "\U00000035\U000020E3", 6: "\U00000036\U000020E3"}


# This method is called when user calls /info command
# It shows available commands
# Also you can add external information into this message
@bot.message_handler(commands=['info'])
def show_info(message):
    info_message = ''
    for i in range(len(bot.get_my_commands())):
        command = bot.get_my_commands()[i]
        info_message += f'/{command.command} - {command.description} \n'
    bot.send_message(message.chat.id, info_message)


# This method is called when user calls /dice command
# It returns a random value from 2 to 12 as sum of dice
# And displays this sum as emoji
@bot.message_handler(commands=['dice'])
def roll_dice(message):
    dice_sum = random.randint(2, 12)
    if dice_sum < 7:
        first_value = random.randint(1, dice_sum - 1)
    else:
        first_value = random.randint(dice_sum - 6, 6)
    second_value = dice_sum - first_value

    first_emoji = ''
    second_emoji = ''
    for i in range(1, 7):
        if i == first_value:
            first_emoji = dice_values_dict.get(i)
        if i == second_value:
            second_emoji = dice_values_dict.get(i)

    game_die_emoji = '\U0001F3B2'

    bot.send_message(message.chat.id,
                     f'The mysterious stranger rolls the {game_die_emoji}{game_die_emoji} '
                     f'and they show {first_emoji}{second_emoji}')


# This method is called when user calls /image command
# It adds a user id into special array
@bot.message_handler(commands=['image'])
def get_image_request(message):
    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name} enter search text',
                     parse_mode='html')
    image_request_users.append(message.from_user.id)


# This method check user input
# If user sent a text message and his id is contained in the special array
# It calls another method to find image finally
@bot.message_handler(content_types=['text'])
def process_user_text_message(message):
    if image_request_users.__contains__(message.from_user.id):
        search_image(message, message.text)
        image_request_users.remove(message.from_user.id)


# This method find image by user request and send back to user
def search_image(message, user_reply):
    url = f'https://www.google.com/search?q={user_reply.lower()}&tbm=isch'
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'xml')
    images = soup.findAll('img')
    image = images[random.randint(0, len(images))]

    bot.send_photo(message.chat.id, image.get('src'))


bot.polling(none_stop=True)
