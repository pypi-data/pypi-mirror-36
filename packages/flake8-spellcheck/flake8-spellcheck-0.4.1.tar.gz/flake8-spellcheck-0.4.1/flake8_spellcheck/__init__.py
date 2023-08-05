# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import tokenize
from string import ascii_lowercase, ascii_uppercase, digits

import pkg_resources


# Really simple detection function
def detect_case(name):
    if "_" in name:
        return "snake"
    else:
        return "camel"


def parse_camel_case(name, col_offset):
    index = col_offset
    buffer = ""
    for c in name:
        if c in ascii_uppercase:
            if buffer:
                yield index - len(buffer), buffer
            buffer = c
        else:
            buffer += c
        index += 1

    if buffer:
        yield index - len(buffer), buffer


def parse_snake_case(name, col_offset):
    index = col_offset
    for token in name.split("_"):
        if token:
            yield index, token
        index += len(token) + 1


class SpellCheckPlugin(object):
    name = "flake8-spellcheck"
    version = "0.4.1"

    def __init__(self, tree, filename="(none)", file_tokens=None):
        self.file_tokens = file_tokens

        self.words = set()
        for dictionary in ("words.txt", "python.txt"):
            data = pkg_resources.resource_string(__name__, dictionary)
            data = data.decode("utf8")
            self.words |= set(w.lower() for w in data.split("\n"))

        if os.path.exists(self.whitelist_path):
            with open(self.whitelist_path, "r") as fp:
                whitelist = fp.read()

            whitelist = set(w.lower() for w in whitelist.split("\n"))
            self.words |= whitelist

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            "--whitelist",
            help="Path to text file containing whitelisted words",
            default="whitelist.txt",
        )

    @classmethod
    def parse_options(cls, options):
        cls.whitelist_path = options.whitelist

    def run(self):
        for token_info in self.file_tokens:
            if token_info.type == tokenize.NAME:
                value = token_info.string
            elif token_info.type == tokenize.COMMENT:
                value = token_info.string.lstrip("#")
            else:
                continue

            tokens = []
            for word in value.split(" "):
                case = detect_case(word)
                if case == "snake":
                    tokens.extend(parse_snake_case(word, token_info.start[1]))
                elif case == "camel":
                    tokens.extend(parse_camel_case(word, token_info.start[1]))

            for index, token in tokens:
                if token.lower() not in self.words:
                    yield (
                        token_info.start[0],
                        index,
                        "SC100 Possibly misspelt word: '{}'".format(token),
                        type(self),
                    )
