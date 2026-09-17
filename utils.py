"""Input helpers with validation and exception handling."""


def input_int(prompt: str, minimum: int | None = None) -> int:
    """Read an integer and repeat the prompt after invalid input."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            suffix = f" не меньше {minimum}" if minimum is not None else ""
            print(f"Введите целое число{suffix}.")
