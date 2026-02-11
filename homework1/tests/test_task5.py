from src import task5
from src.task5 import main

def test_book_list():
    assert isinstance(task5.my_favorite_books,list)

def test_student_dict():
    assert isinstance(task5.my_students, dict)

def test_first_three_books(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "['The Great Gatsby', 'To Kill a Mockingbird', '1984']\n"