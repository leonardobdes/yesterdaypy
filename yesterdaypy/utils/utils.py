ERRORS = {
    1: "Environment variable LINODE_TOKEN not setup",
    2: "error 2 text"
}


def error(code: int) -> None:
    """"Prints an error text and exits."""
    print(f"Error {code}: {ERRORS[code]}.")
    exit(code)
