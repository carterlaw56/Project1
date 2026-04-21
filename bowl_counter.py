import csv

FILE_NAME = "nutrition_info.csv"


def load_data():
    data = []
    with open(FILE_NAME, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["calories"] = int(row["calories"])
            row["protein"] = int(row["protein"])
            row["carbs"] = int(row["carbs"])
            row["fat"] = int(row["fat"])
            data.append(row)
    return data


def group_by_category(data):
    categories = {}
    for item in data:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    return categories


def choose_one(category_name, items, allow_none=True):
    print(f"\n--- {category_name.upper()} ---")

    option_map = {}

    number = 1
    for item in items:
        print(f"{number}. {item['item_name']} ({item['calories']} cal)")
        option_map[str(number)] = item
        number += 1

    if allow_none:
        print(f"{number}. None")
        option_map[str(number)] = None

    while True:
        choice = input("Choose one number: ").strip()
        if choice in option_map:
            return option_map[choice]
        print("Invalid choice. Try again.")


def choose_multiple(category_name, items):
    print(f"\n--- {category_name.upper()} ---")

    option_map = {}
    number = 1

    for item in items:
        print(f"{number}. {item['item_name']} ({item['calories']} cal)")
        option_map[str(number)] = item
        number += 1

    print(f"{number}. None")

    print("Choose as many as you want.")
    print("Type numbers separated by commas like: 1,3,4")
    print("Or type the number for None.")

    while True:
        choice = input("Your choices: ").strip()

        if choice == str(number):
            return []

        if choice == "":
            return []

        parts = [x.strip() for x in choice.split(",")]
        selected = []
        valid = True

        for part in parts:
            if part in option_map:
                selected.append(option_map[part])
            else:
                valid = False
                break

        if valid:
            return selected

        print("Invalid choice. Try again.")


def calculate_totals(selected):
    totals = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }

    for item in selected:
        totals["calories"] += item["calories"]
        totals["protein"] += item["protein"]
        totals["carbs"] += item["carbs"]
        totals["fat"] += item["fat"]

    return totals


def main():
    data = load_data()
    categories = group_by_category(data)
    selected_items = []

    print("Welcome to the Chipotle Nutrition Calculator")

    # Base: Bowl or Burrito
    base_choice = choose_one("Base", categories["base"], allow_none=False)
    selected_items.append(base_choice)

    # One choice with None option
    rice_choice = choose_one("Rice", categories["rice"], allow_none=True)
    if rice_choice:
        selected_items.append(rice_choice)

    beans_choice = choose_one("Beans", categories["beans"], allow_none=True)
    if beans_choice:
        selected_items.append(beans_choice)

    protein_choice = choose_one("Protein", categories["protein"], allow_none=True)
    if protein_choice:
        selected_items.append(protein_choice)

    # Multiple choice toppings with None option
    for category in ["veggies", "salsa", "dairy", "extras"]:
        if category in categories:
            choices = choose_multiple(category, categories[category])
            selected_items.extend(choices)

    totals = calculate_totals(selected_items)

    print("\n--- YOUR ORDER ---")
    for item in selected_items:
        print(f"- {item['item_name']}")

    print("\n--- TOTAL NUTRITION ---")
    print(f"Calories: {totals['calories']}")
    print(f"Protein: {totals['protein']}g")
    print(f"Carbs: {totals['carbs']}g")
    print(f"Fat: {totals['fat']}g")


if __name__ == "__main__":
    main()