from textnode import TextType, TextNode


def main():
    try:
        new_textnode = TextNode("This is some text", TextType.BOLD, "http://someurl.com")
        print(new_textnode)
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()
