def extract_uuid(config_key: str) -> str:
    try:
        return config_key.split("vless://")[1].split("@")[0]
    except IndexError:
        return "Неизвестно"

def get_time_word(value: int, words: tuple) -> str:
    if value % 10 == 1 and value % 100 != 11:
        return words[0]
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return words[1]
    else:
        return words[2]