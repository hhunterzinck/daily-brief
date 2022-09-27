class Greeter:
    """Creates a greeter object that greets people."""

    def __init__(self, name):
        self.name = name

    def say_hello(self, time_of_day: str) -> str:
        """Say hello.

        Args:
            name (str): name of a person
            other (str): another name or entity
        Returns:
            str: string that is printed
        """

        print_str = f"Good {time_of_day}, {self.name}!"
        print(print_str)
        return print_str

    def say_bye(self, friend: str) -> str:
        """Say bye.

        Args:
            name (str): name of a person
            friend (str): another name or entity
        Returns:
            str: string that is printed
        """

        print_str = f"Bye, {self.name} and {friend}!"
        print(print_str)
        return print_str
