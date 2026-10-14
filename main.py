import csv
import os
from difflib import SequenceMatcher

FILE = "lost_found.csv"

FIELDS = [
    "id", "status", "item", "description",
    "location", "date", "contact"
]


def load_items():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_item(item):
    file_exists = os.path.exists(FILE)

    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        if not file_exists or os.path.getsize(FILE) == 0:
            writer.writeheader()

        writer.writerow(item)


def add_item():
    status = input("Type lost or found: ").strip().lower()

    if status not in ["lost", "found"]:
        print("Please enter lost or found.")
        return

    items = load_items()

    item = {
        "id": str(len(items) + 1),
        "status": status,
        "item": input("Item name: ").strip(),
        "description": input("Description: ").strip(),
        "location": input("Location: ").strip(),
        "date": input("Date (YYYY-MM-DD): ").strip(),
        "contact": input("Contact (optional): ").strip()
    }

    if not item["item"] or not item["description"]:
        print("Item name and description are required.")
        return

    save_item(item)
    print("Report saved successfully!")


def find_matches():
    items = load_items()
    search_id = input("Enter the report ID to find matches: ").strip()

    selected = next(
        (x for x in items if x["id"] == search_id), None
    )

    if selected is None:
        print("Report not found.")
        return

    opposite = "found" if selected["status"] == "lost" else "lost"
    candidates = []

    for other in items:
        if other["status"] != opposite:
            continue

        text1 = (
            selected["item"] + " " + selected["description"]
        ).lower()

        text2 = (
            other["item"] + " " + other["description"]
        ).lower()

        similarity = SequenceMatcher(
            None, text1, text2
        ).ratio()

        if selected["location"].lower() == other["location"].lower():
            similarity += 0.15

        similarity = min(similarity, 1.0)

        candidates.append((similarity, other))

    candidates.sort(key=lambda x: x[0], reverse=True)

    if not candidates:
        print("No opposite-type reports are available yet.")
        return

    print("\nPossible matches:")

    for score, match in candidates:
        print("-" * 35)
        print("Report ID:", match["id"])
        print("Status:", match["status"])
        print("Item:", match["item"])
        print("Description:", match["description"])
        print("Location:", match["location"])
        print("Similarity score:", round(score * 100), "%")

    print("\nScores are suggestions, not proof of a match.")


def view_reports():
    items = load_items()

    if not items:
        print("No reports have been added.")
        return

    for item in items:
        print("-" * 35)
        for field in FIELDS[:-1]:
            print(field.title() + ":", item[field])


def main():
    while True:
        print("\n=== Campus Lost & Found Matcher ===")
        print("1. Report a lost or found item")
        print("2. Find possible matches")
        print("3. View all reports")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_item()
        elif choice == "2":
            find_matches()
        elif choice == "3":
            view_reports()
        elif choice == "4":
            print("Thank you!")
            break
        else:
            print("Invalid option. Choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()