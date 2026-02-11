from src.task6 import main

def test_word_count(capsys):
    word_count = main()
    assert word_count == 104
