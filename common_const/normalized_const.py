@staticmethod
def punctuation_list():
    return ['。', '！', '？', '；', '\.', '!', '\?', ';', '，', ',', ' ']


def symbols_regular_list():
    return "[^\u4e00-\u9fa5^a-z^A-Z^0-9^\s^\n^,^\.^:^;^!^?^~^\-^—^-^,^、^。^:^；^！^？^《^》^<^>^（^）^()^“^”^' '^\"^\[\]^\{^\}]"
