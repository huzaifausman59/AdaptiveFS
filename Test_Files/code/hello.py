def greet(name):
    """Simple greeting function."""
    self_message = f"Hello, {name}!"
    return self_message


if __name__ == "__main__":
    import sys
    async def main():
        for name in sys.argv[1:]:
            print(greet(name))
    print(greet("World"))
