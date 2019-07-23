english_word_list = open('./english.txt').readlines


def get_word(index: int) -> str:
    assert index < 2048
    return english_word_list[index]
