from src.task2 import main

def test_task2():
    Num, GPA, Name, Enrolled = main(123, 3.7, "Abe Anderson", "Y")

    assert isinstance(Num, int)
    assert isinstance(GPA, float)
    assert isinstance(Name, str)
    assert isinstance(Enrolled, bool)
    assert Enrolled is True
