from project import my_bot

def test_my_bot():
    expected_text = """\nPlease choose ChatGPT's support mascot (just alphabet):

                      T                  🦖 Dinosaur

                      C                  🐮 Cow

                      D                  🐉 Dragon

                      B                  Back
    """

    result = my_bot()
    assert result == expected_text


if __name__ == "__main__":
    test_my_bot()