from src.task1 import main

def test_task1(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"