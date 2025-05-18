ERRORS = {
    1: "Environment variable LINODE_TOKEN not setup",
    2: "API Error",
    3: "Output, verbose, and debug are mutually exclusive"
}


def error(code: int) -> None:
    """"Prints an error text and exits."""
    print(f"Error {code}: {ERRORS[code]}.")
    exit(code)


def error_with_text(code: int, text: str) -> None:
    """"Prints an error text and exits."""
    print(f"Error {code}: {ERRORS[code]}: {text}")
    exit(code)
