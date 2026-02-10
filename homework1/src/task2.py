def main(S_Num, S_GPA, S_Name, enrolled_input):
    """generates a student based on input"""
    enrolled_input = enrolled_input.strip().upper()
    S_enrolled = enrolled_input == "Y"

    return S_Num, S_GPA, S_Name, S_enrolled


if __name__ == "__main__":
    print("Enter Student Details:\n")
    S_Num = int(input("Student Num: "))
    S_GPA = float(input("Student GPA: "))
    S_Name = input("Student Name: ")
    enrolled_input = input("Enroll student? (Y or N): ")

    result = main(S_Num, S_GPA, S_Name, enrolled_input)
    print(result)
