import database
db = database.SQLiter("db.db")


english_chars = {'a': '•–', 'b': '–•••', 'c': '–•–•', 'd': '–••', 'e': '•', 'f': '••–•', 'g': '––•', 'h': '••••',
                 'i': '••', 'j': '•–––', 'k': '–•–', 'l': '•–••', 'm': '––', 'n': '–•', 'o': '–––', 'p': '•––•',
                 'q': '––•–', 'r': '•–•', 's': '•••', 't': '–', 'u': '••–', 'v': '•••–', 'w': '•––', 'x': '–••–',
                 'y': '–•––', 'z': '––••', '0': '–––––', '1': '•––––', '2': '••–––', '3': '•••––', '4': '••••–',
                 '5': '•••••', '6': '–••••', '7': '––•••', '8': '–––••', '9': '––––•', '.': '•–•–•–', ',': '––••––',
                 '?': '••––••', "'": '•––––•', '!': '–•–•––', '/': '–••–•', '(': '–•––•', ')': '–•––•–', '&': '•–•••',
                 ':': '–––•••', ';': '–•–•–•', '=': '–•••–', '+': '•–•–•', '-': '–••••–', '_': '••––•–', '"': '•–••–•',
                 '$': '•••–••–', '@': '•––•–•'}

russian_chars = {'а': '•–', 'б': '–•••', 'в': '•––', 'г': '––•', 'д': '–••', 'е': '•', 'ж': '•••–', 'з': '––••',
                 'и': '••', 'й': '•–––', 'к': '–•–', 'л': '•–••', 'м': '––', 'н': '–•', 'о': '–––', 'п': '•––•',
                 'р': '•–•', 'с': '•••', 'т': '–', 'у': '••–', 'ф': '••–•', 'х': '••••', 'ц': '–•–•', 'ч': '–––•',
                 'ш': '––––', 'щ': '––•–', 'ъ': '––•––', 'ы': '–•––', 'ь': '–••–', 'э': '••–••', 'ю': '••––',
                 'я': '•–•–',
                 '0': '–––––', '1': '•––––', '2': '••–––', '3': '•••––', '4': '••••–', '5': '•••••', '6': '–••••',
                 '7': '––•••', '8': '–––••', '9': '––––•',
                 '.': '•–•–•–', ',': '––••––', '?': '••––••', "'": '•––––•', '!': '–•–•––', '/': '–••–•', '(': '–•––•',
                 ')': '–•––•–', '&': '•–•••', ':': '–––•••', ';': '–•–•–•', '=': '–•••–', '+': '•–•–•', '-': '–••••–',
                 '_': '••––•–', '"': '•–••–•', '$': '•••–••–', '@': '•––•–•'}

reversed_english = {v: k for k, v in english_chars.items()}
reversed_russian = {v: k for k, v in russian_chars.items()}  # поменять местами ключ и значение


async def start_msg(usr):  # стартовое сообщение
    data = db.select_all_for_user(usr)  # запрос настроек для пользователя
    return f"Your settings:\n\n\
           Language: {data[1]}\n\
           Dot: {data[2]}\n\
           Dash: {data[3]}\n\
           Mode: {data[4]}\n\n\
           Commands:\n\
           /settings - change your settings.\n\
           /reset - reset the default settings\n\n\
           Also you can send text to translate. I\'ll do my best."


async def edit_settings_msg(usr):  # редактируемое сообщение настроек
    dt = db.select_all_for_user(usr)  # запрос настроек для пользователя
    return f'The settings have been saved.\n\nLanguage: {dt[1]}\nDot: {dt[2]}\nDash: {dt[3]}\nMode: {dt[4]}'


async def translator(usr, msg):  # переводчик с аргументами user_id и message.text
    data = db.select_all_for_user(usr)  # запрос настроек для пользователя
    if msg and data[4] == 'Morse':  # если режим Морзе
        if data[1] == 'English':  # если язык английский
            result = ''
            for word in msg.lower().split():
                result += '  '
                for char in word:
                    try:
                        # попытаться записать в результат изменив значение в словаре на значения в настройках
                        result += english_chars[char].replace('•', data[2]).replace('–', data[3]) + ' '
                    except KeyError:
                        # если соответствия нет, дать знать пользователю, что нужно сделать и чего нельзя
                        return "In this <b>mode</b> use only chars such as\n\n\
 <b>abcdefghijklmnopqrstuvwxyz\n0123456789.,?'!/()&:;=+-_\"$@</b>\nor change the /settings"
            if len(result) >= 4096:  # если сообщение больше или равно 4096 символов, уведомить об ограничении телеграм
                return f"The result size is {len(result)} characters.\
 The maximum size should not exceed <b>4096</b> characters."
            return result.strip()  # вернуть результат
        else:
            result = ''
            for word in msg.lower().split():
                result += '  '
                for char in word.replace('ё', 'е'):  # заменить ё на е, так как в азбуке Морзе нет буквы ё
                    try:
                        result += russian_chars[char].replace('•', data[2]).replace('–', data[3]) + ' '
                    except KeyError:
                        return "In this <b>mode</b> use only chars such as\n\n\
 <b>абвгдежзийклмнопрстуфхцчшщъыьэюя\n0123456789.,?'!/()&:;=+-_\"$@</b>\n\nChange the /settings"
            if len(result) >= 4096:
                return f"The result size is {len(result)} characters.\
 The maximum size should not exceed <b>4096</b> characters."
            return result.strip()

    elif msg and data[4] == 'Text':  # если режим текст
        if data[1] == 'English':  #
            result = ' '
            # пройтись циклом по сообщению, разделив слова по пробелам и заменив значения настроек на значения словаря
            for word in msg.replace(data[2], '•').replace(data[3], '–').split(' '):
                if word in reversed_english.keys():  # если код есть в ключах словаря
                    result += reversed_english[word]  # записать результат из словаря
                elif word == '':  # если пустая строка
                    result += ' '  # добавить пробел
                elif word not in reversed_english.keys():  # если в ключах нет соответствия, уведомить пользователя
                    return "Use only Morse code in this <b>mode</b>\n\nChange the /settings"
            if len(result) >= 4096:
                return f"The result size is {len(result)} characters.\
 The maximum size should not exceed <b>4096</b> characters."
            return result.strip().replace("  ", " ")  # вернуть результат
        else:
            result = ' '
            for word in msg.replace(data[2], '•').replace(data[3], '–').split(' '):
                if word in reversed_russian.keys():
                    result += reversed_russian[word]
                elif word == '':
                    result += ' '
                elif word not in reversed_russian.keys():
                    return "Use only Morse code in this <b>mode</b>\nor change the /settings"
            if len(result) >= 4096:
                return f"The result size is {len(result)} characters.\
 The maximum size should not exceed <b>4096</b> characters."
            return result.strip().replace("  ", " ")
