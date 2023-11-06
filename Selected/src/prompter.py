from typing import TypeVar, Type, Callable, Optional

T = TypeVar("T")


class Prompter:
    def __init__(
        self,
        prompt: str,
        required: bool = True,
        input_type: Type[T] = str,
        validation_func: Optional[Callable[[T], bool]] = None,
    ):
        self.prompt = prompt
        self.required = required
        self.input_type = input_type
        self.validation_func = validation_func

    def ask(self) -> T:
        """
        Ask the user for input, and return the result. If the user enters an
        empty string, and the prompt is required, ask again. If the user enters
        an empty string, and the prompt is not required, return None. If the user
        enters a value, return the value converted to the type specified in the
        constructor. If a custom validation_func is provided, use it to validate.
        """

        while True:
            user_input = input(self.prompt + ": ")
            if user_input == "" and self.required:
                print("You must enter a value")
                continue
            elif user_input == "" and not self.required:
                return None
            else:
                try:
                    converted_value = self.input_type(user_input)
                    if not isinstance(converted_value, self.input_type):
                        raise ValueError("Invalid value")
                    if self.validation_func:
                        success = self.validation_func(converted_value)
                        if not success:
                            raise ValueError("Invalid value")
                    return converted_value
                except ValueError:
                    print("You must enter a valid value")
                    continue
