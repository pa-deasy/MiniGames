END_MESSAGE = '\n--------------------------\n'

def print_message(message: str) -> None:
    print(message)
    print(END_MESSAGE)
    

def print_message_and_get_input(message: str) -> str:
    input_message = input(message)
    print(END_MESSAGE)
    return input_message
