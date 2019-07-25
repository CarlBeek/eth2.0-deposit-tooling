english_word_list = open('key_derivation/mnemonic/english.txt').readlines()


def get_word(index: int) -> str:
    assert index < 2048
    return english_word_list[index][:-1]
