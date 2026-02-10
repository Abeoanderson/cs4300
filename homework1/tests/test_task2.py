from src.task2 import main

def test_task2():
    Num, GPA, Name, Enrolled = main()
    assert(Num, int)
    assert(GPA, float)
    assert(Name, string)
    assert(Enrolled, bool)