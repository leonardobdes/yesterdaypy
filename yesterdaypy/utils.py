ERRORS = {
    1: "Environment variable LINODE_TOKEN not setup",
}


def error(code: int) -> None:
    """"Prints an error text and exits."""
    print(f"Error {code}: {ERRORS[code]}.")
    exit(code)
