import os
import openai
import sys
import re
import cowsay
import json
import csv
import textwrap
from tabulate import tabulate
from pyfiglet import figlet_format
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep, gmtime, strftime
filename = "history_chat.csv"
white_space = "                "
colors = {
    'reset': '\x1b[0m',
  'bold': '\x1b[1m',
  'italic': '\x1b[3m',
  'underline': '\x1b[4m',
  'inverse': '\x1b[7m',
  'black': '\x1b[30m',
  'red': '\x1b[31m',
  'green': '\x1b[32m',
  'yellow': '\x1b[33m',
  'blue': '\x1b[34m',
  'magenta': '\x1b[35m',
  'cyan': '\x1b[36m',
  'white': '\x1b[37m',
  'gray': '\x1b[90m',
  'bright_red': '\x1b[91m',
  'bright_green': '\x1b[92m',
  'bright_yellow': '\x1b[93m',
  'bright_blue': '\x1b[94m',
  'bright_magenta': '\x1b[95m',
  'bright_cyan': '\x1b[96m',
  'bright_white': '\x1b[97m',
  'bg_black': '\x1b[40m',
  'bg_red': '\x1b[41m',
  'bg_green': '\x1b[42m',
  'bg_yellow': '\x1b[43m',
  'bg_blue': '\x1b[44m',
  'bg_magenta': '\x1b[45m',
  'bg_cyan': '\x1b[46m',
  'bg_white': '\x1b[47m',
  'bg_gray': '\x1b[100m',
  'bg_bright_red': '\x1b[101m',
  'bg_bright_green': '\x1b[102m',
  'bg_bright_yellow': '\x1b[103m',
  'bg_bright_blue': '\x1b[104m',
  'bg_bright_magenta': '\x1b[105m',
  'bg_bright_cyan': '\x1b[106m',
  'bg_bright_white': '\x1b[107m'
}

def main():
    start_program()

class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


def load_api_key(secrets_file="secrets.json"):
    with open(secrets_file) as f:
        secrets = json.load(f)
    return secrets["OPENAI_API_KEY"]

def history_conversations_function():
    conversations = []
    with open(filename) as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader):
            limit = 10
            if index <= limit:
                conversations.append({"date": row["date"], "me": row["me"], "bot": row["bot"]})
        for chat in sorted(conversations, key=lambda chat: chat["date"]):
            yield chat["date"], chat["me"], chat["bot"]


def start_program():
    try:

        if sys.argv[1] == "-s":
            serve_program()

        elif sys.argv[1] == "-i":
            print(f"""{colors["bright_green"]}Welcome to the Chat GPT Clone project! This Python program allows you to interact with a chatbot that utilizes the power of GPT (Generative Pre-trained Transformer) models.
            The chatbot is designed to provide answers based on a given input question using the GPT Chat API. It leverages the capabilities of GPT, a state-of-the-art language model developed by OpenAI, to generate human-like responses and engage in dynamic conversations.

            With this project, you can experience firsthand the capabilities of GPT in a chatbot scenario. You can ask any question you like, and the chatbot will use the GPT Chat API to provide relevant and context-aware answers.

            Instructions:
            1. Run the Python script using the command: python project.py -i
            2. Once the program starts, you will see the project introduction.
            3. Follow the prompts to interact with the chatbot.
            4. Input your questions and wait for the chatbot's response.
            5. Enjoy engaging in dynamic conversations with the GPT-powered chatbot!

            Note: Ensure that you have a stable internet connection to access the GPT Chat API.

            Now, let's dive into the world of conversational AI with the Chat GPT Clone project. Get ready to explore the capabilities of GPT and have engaging conversations with the chatbot! \n {colors["reset"]}""")

        elif sys.argv[1] == "-c":
            header_history_conversation_table = ["date", "me", "bot"]
            result_history_conversation_table = []
            for s in history_conversations_function():
                result_history_conversation_table.append([s[0], textwrap.fill(s[1], 35), textwrap.fill(s[2], 70)])
            print(tabulate(result_history_conversation_table, header_history_conversation_table, tablefmt="heavy_grid"))


        elif sys.argv[1] == "-help":
            print(f"""Options:
            {colors["bright_green"]}-s{colors["reset"]}{white_space}Run Program
            {colors["bright_green"]}-i{colors["reset"]}{white_space}Introduction to Program
            {colors["bright_green"]}-c{colors["reset"]}{white_space}Conversations History
                  """)

        else:
            raise ValueError

    except (ValueError, IndexError):
        print(f'\n{colors["red"]}ValueError: No syntax is available at the moment, you may need -help for assistance.\n {colors["reset"]}')

def serve_program():
    class Type_serve:
        def __init__(self, type):
            self._type = type

        def __str__(self):
            return self._type

        @property
        def type(self):
            return self._type
    wellcome_figlet = figlet_format("ChatGPT", font = "banner3-D")
    print(wellcome_figlet)
    while True:
        print(f"""
              {Type_serve(f'{colors["bright_green"]}2{colors["reset"]}{white_space}DALL·ECreate realistic images and art from a description in natural language')}

              {Type_serve(f'{colors["bright_green"]}1{colors["reset"]}{white_space}ChatGPT Interact with our flagship language models in a conversational interface')}

              {Type_serve(f'{colors["bright_green"]}0{colors["reset"]}{white_space}{colors["underline"]}Cancel{colors["reset"]}')}
              """)
        choose_serve = input("what program do you choose (just number only)?: ").strip()
        match choose_serve:
            case "2":
                return cowsay.cow("This feature is under maintenance, please come back later\n")
            case "1":
                    while True:
                        loader = Loader("Loading...", my_bot() , 0.05).start()
                        for _ in range(10):
                            sleep(0.10)
                        loader.stop()
                        answer_for_mascot = input("Input here: ").upper().strip()
                        prompt_out_side = f"""



                                                                    ChatGPT

                                 Examples                         Capabilities                      Limitations
                        "Explain quantum computing in       Remembers what user said          May occasionally generate
                                simple terms" →             earlier in the conversation         incorrect information
                                    ...                                ...                               ...

                        \n{colors["underline"]}*** If you want to exit the program, type command: "///exit///" ***{colors["reset"]} \n
                        """
                        match answer_for_mascot:
                            case "T":
                                return create_prompt("🦖", prompt_out_side)
                            case "C":
                                return create_prompt("🐮", prompt_out_side)
                            case "D":
                                return create_prompt("🐉", prompt_out_side)
                            case "B":
                                break
                            case _:
                                print(f'{colors["red"]}Please try again, just choose alphabet (e.g >>> T){colors["reset"]}')
            case "0":
                sys.exit(0)

            case _:
                print(f'{colors["red"]}Please try again, just choose number (e.g >>> 1){colors["reset"]}')

def my_bot():

    text = f"""\nPlease choose ChatGPT's support mascot (just alphabet):

                      T                  🦖 Dinosaur

                      C                  🐮 Cow

                      D                  🐉 Dragon

                      B                  Back
    """
    return text

def create_prompt(bot, prompt_out_side):
    try:
        loader = Loader("Loading...", prompt_out_side , 0.05).start()
        for _ in range(10):
            sleep(0.10)
        loader.stop()

        while True:
            send_message = input(f'{colors["gray"]}Send a message: {colors["reset"]}').strip()
            if re.search(r"^\"?\/\/\/exit\/\/\/\"?$", send_message):
                sys.exit(0)
            else:
                loader = Loader("Currently pending by AI...", "" , 0.05).start()
                for _ in range(10):
                    sleep(0.10)
                api_key = load_api_key()
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                temperature = 0.2,
                max_tokens = 2000,
                messages = [
                    {"role": "user", "content": send_message}
                ]
                )
                loader.stop()
                result = f'{colors["bright_green"]}{bot} says: {colors["reset"]}{response["choices"][0]["message"]["content"]}\n'
                print(result)

                headers = ["date", "me", "bot"]
                file_exists = os.path.isfile(filename)
                with open (filename, 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)
                    if not file_exists:
                        writer.writeheader()
                    a = " ".join(line.strip() for line in response["choices"][0]["message"]["content"].splitlines())
                    writer.writerow({"date": strftime("%Y-%m-%d %H:%M:%S", gmtime()), "me": send_message, "bot": a})

    except:
        sys.exit(1)


if __name__ == "__main__":
    main()
