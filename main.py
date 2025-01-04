import sys
from abc import ABC, abstractmethod


class GroceriesInterface(ABC):
    """Interface for managing groceries."""

    @abstractmethod
    def add_item(self, item: str) -> None:
        pass

    @abstractmethod
    def remove_item(self, item: str) -> None:
        pass

    @abstractmethod
    def display(self) -> None:
        pass


class GroceriesManager(GroceriesInterface):
    """Manages groceries in memory."""

    def __init__(self):
        self.groceries = []

    def add_item(self, item: str) -> None:
        self.groceries.append(item)
        print(f'"{item}" has been added!')

    def remove_item(self, item: str) -> None:
        try:
            self.groceries.remove(item)
            print(f'"{item}" has been removed!')
        except ValueError:
            print(f'No "{item}" found in the list.')

    def display(self) -> None:
        if not self.groceries:
            print("The groceries list is empty.")
        else:
            print("---- Grocery List ----")
            for i, item in enumerate(self.groceries, 1):
                print(f"{i}: {item.capitalize()}")
            print("-" * 25)


class FileGroceriesManager(GroceriesInterface):
    """Manages groceries stored in a file."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def _read_file(self) -> list[str]:
        try:
            with open(self.file_path, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def _write_file(self, groceries: list[str]) -> None:
        with open(self.file_path, 'w') as file:
            file.write("\n".join(groceries))

    def add_item(self, item: str) -> None:
        groceries = self._read_file()
        groceries.append(item)
        self._write_file(groceries)
        print(f'"{item}" has been added!')

    def remove_item(self, item: str) -> None:
        groceries = self._read_file()
        try:
            groceries.remove(item)
            self._write_file(groceries)
            print(f'"{item}" has been removed!')
        except ValueError:
            print(f'No "{item}" found in the file.')

    def display(self) -> None:
        groceries = self._read_file()
        if not groceries:
            print("The groceries list is empty.")
        else:
            print("---- Grocery List (File) ----")
            for i, item in enumerate(groceries, 1):
                print(f"{i}: {item.capitalize()}")
            print("-" * 25)


def welcome_msg() -> None:
    """Displays the welcome message."""
    print('Welcome to Groceries!')
    print('Enter:')
    print('-----------------------')
    print('1 - To add an item')
    print('2 - To remove an item')
    print('3 - To list all items')
    print('0 - To exit the program')
    print('-----------------------')


def is_valid_option(option: str) -> bool:
    """Checks if the user input is a valid option."""
    return option in ['1', '2', '3', '0']


def main() -> None:
    """Main function to run the groceries program."""
    print("Choose your storage option:")
    print("1 - Manage groceries in memory")
    print("2 - Manage groceries in a file")
    option = input("Enter your choice: ").strip()

    if option == "1":
        manager: GroceriesInterface = GroceriesManager()
    elif option == "2":
        file_path = "groceries.txt"
        manager: GroceriesInterface = FileGroceriesManager(file_path)
    else:
        print("Invalid option. Exiting.")
        return

    welcome_msg()

    while True:
        user_input: str = input("Choose your option: ").strip()

        if not is_valid_option(user_input):
            print("Please pick a valid option.")
            continue

        if user_input == "1":
            new_item: str = input("What item would you like to add? >> ").strip().lower()
            if not new_item:
                print("You cannot add an empty value.")
            else:
                manager.add_item(new_item)

        elif user_input == "2":
            remove_item_name: str = input("What item would you like to remove? >> ").strip().lower()
            manager.remove_item(remove_item_name)

        elif user_input == "3":
            manager.display()

        elif user_input == "0":
            print("Exiting the program.")
            sys.exit()


if __name__ == '__main__':
    main()
