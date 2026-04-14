def vote_menu():
    print("*****************")
    print("Voting Menu")
    print("*****************")
    print("press 'v' to vote")
    print("press 'x' to exit program")

    while True:
        choice = input("Option: ").strip().lower()
        if choice in ("v", "x"):
            return choice
        choice = input("Invalid (v/x): ").strip().lower()
        if choice in ("v", "x"):
            return choice


def candidate_menu():
    print("*****************")
    print("Candidate Menu")
    print("*****************")
    print("1: Isabella")
    print("2: Genji")
    print("3: Hannah")

    while True:
        choice = input("Candidate: ").strip()
        if choice.isdigit() and int(choice) in (1, 2, 3):
            num = int(choice)
        
        choice = input("Invalid (1/2/3): ").strip()
        if choice.isdigit() and int(choice) in (1, 2, 3):
            num = int(choice)


def main():
    isabella = 0
    genji = 0
    hannah = 0
    total = 0

    while True:
        choice = vote_menu()

        if choice == 'x':
            print("-------------------------------------------------------")
            print(f'Isabella = {isabella}, Genji = {genji}, Hannah = {hannah}, Total = {total}')
            print("-------------------------------------------------------")
            return

        candidate = candidate_menu()

        if candidate == 1:
            isabella += 1
            print("Voted Isabella")
        elif candidate == 2:
            genji += 1
            print("Voted Genji")
        elif candidate == 3:
            hannah += 1
            print("Voted Hannah")

        total += 1


main()