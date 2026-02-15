from src.task6 import count_num_lines

def test_word_count(capsys):
    word_count = count_num_lines()
    assert word_count == 104
