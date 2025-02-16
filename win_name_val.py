import random
import string

import regex as rx


class WindowsNameValidator:
    def __init__(self, title):
        self.title = title
        self.RESERVED_NAMES = {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM0",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT0",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        }

    # trace: Motorcycle 4K 120fps | HDR
    def clean_title(self):
        if rx.search(r'[<>:"/\|?*]', self.title):
            self.title = self.remove_ivld_chars()  # Motorcycle 4K 120fps  HDR
        if rx.search(r"(\s{2,})", self.title):
            self.title = self.remove_csct_space()  # Motorcycle 4K 120fps HDR
        if rx.search(r"\p{C}", self.title):
            self.title = self.remove_ctrl_chars()  # Motorcycle 4K 120fps HDR
        if self.title.upper() in self.RESERVED_NAMES:
            self.title = self.remove_resv_names()
        if self.title.startswith((".", " ")):
            self.title = self.remove_start_chars()
        if self.title.endswith((".", " ")):
            self.title = self.remove_end_chars()
        return self.title

    def remove_ivld_chars(self):
        return rx.sub(r'[<>:"/\|?*]', " ", self.title)

    def remove_csct_space(self):  # remove consecutive middle spaces
        return rx.sub(r"(\s{2,})", " ", self.title)

    def remove_ctrl_chars(self):
        return rx.sub(r"\p{C}", " ", self.title)

    def randomizer(self, chars_pool):
        rand_chars = "".join(random.choice(chars_pool) for i in range(10))
        return rand_chars

    def remove_resv_names(self):
        chars_pool = string.ascii_letters + string.digits
        return self.title.replace(self.title, self.randomizer(chars_pool))

    def remove_start_chars(self):
        while True:
            self.title = self.title[1:]  # remove first char
            return self.title

    def remove_end_chars(self):
        while True:
            self.title = self.title[:-1]  # remove last char
            return self.title
