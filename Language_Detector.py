import os
KEYWORD_HINTS = {
    "Python": [
        "def ", "from ", "import ", "__name__", "__main__",
        "lambda ", "self", "elif ", "yield ", "async def", "await "
    ],

    "JavaScript": [
        "function ", "console.log", "const ", "let ", "=>",
        "document.", "window.", "module.exports", "require("
    ],

    "TypeScript": [
        "interface ", "type ", "readonly ", "enum ",
        "implements ", ": string", ": number", ": boolean"
    ],

    "Java": [
        "public class", "public static void main",
        "System.out.println", "package ", "import java",
        "@Override", "implements ", "extends "
    ],

    "C": [
        "printf(", "scanf(",
        "malloc(", "free(", "int main("
    ],

    "C++": [
         "std::", "cout <<", "cin >>",
        "using namespace std", "template<", "vector<"
    ],

    "C#": [
        "using System", "namespace ",
        "Console.WriteLine", "Console.ReadLine",
        "public static void Main"
    ],

    "Go": [
        "package main", "func main",
        "fmt.", "go ", "defer ", "chan "
    ],

    "Rust": [
        "fn main", "println!",
        "let mut", "use std", "impl "
    ],

    "Ruby": [
        "def ", "puts ",
        "end", "require ",
        "class ", "module "
    ],

    "PHP": [
        "<?php", "echo ",
        "$_POST", "$_GET",
        "$_SESSION", "$this->"
    ],

    "Swift": [
        "import Swift", "func ",
        "let ", "var ",
        "guard ", "struct "
    ],

    "Kotlin": [
        "fun main", "val ",
        "var ", "println(",
        "object "
    ],

    "Shell": [
        "#!/bin/bash", "#!/bin/sh",
        "echo ", "chmod ",
        "export "
    ],

    "SQL": [
        "SELECT ", "INSERT INTO",
        "UPDATE ", "DELETE FROM",
        "CREATE TABLE", "ALTER TABLE"
    ],

    "HTML": [
        "<html", "<head",
        "<body", "<!DOCTYPE html"
    ],

    "CSS": [
        "color:", "background:",
        "font-size:", "margin:",
        "padding:"
    ],

    "SCSS": [
        "$", "@mixin",
        "@include", "@extend"
    ],

    "R": [
        "<-", "library(",
        "data.frame", "ggplot("
    ],

    "Lua": [
        "function ", "local ",
        "end", "require("
    ],

    "Perl": [
        "#!/usr/bin/perl",
        "use strict",
        "use warnings",
        "my $"
    ],
}


EXTENSION_MAP ={
    "py": "Python",
    "js": "JavaScript",
    "ts": "TypeScript",
    "jsx": "JavaScript",
    "tsx": "TypeScript",
    "java": "Java",
    "c": "C",
    "cpp": "C++",
    "h": "C",
    "hpp": "C++",
    "cs": "C#",
    "go": "Go",
    "rs": "Rust",
    "rb": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "kt": "Kotlin",
    "sh": "Shell",
    "bash": "Shell",
    "sql": "SQL",
    "html": "HTML",
    "css": "CSS",
    "scss": "SCSS",
    "r": "R",
    "lua": "Lua",
    "pl": "Perl",
    "ipynb": "Python"
}

def detect_programming_language(file_path):
    """
    Detect the programming language of a source code file using
    full keyword scoring across all languages — most accurate,
    since it always finds the single best match rather than
    settling for the first plausible one.
    Checks extension first, but only trusts it if at least 1
    keyword for that language is found in the content. If the
    extension is unknown, or fails that check, falls back to
    scoring all languages.
    """
    extension = os.path.splitext(file_path)[1].lower().lstrip(".")
    extension_language = EXTENSION_MAP.get(extension)

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read(4096).lower()
    except Exception as e:
        print(f"Error reading source code file '{file_path}': {e}")
        return extension_language or "Unknown"

    # Extension known — verify with at least 1 matching keyword
    if extension_language:
        keywords = KEYWORD_HINTS.get(extension_language, [])
        if any(keyword.lower() in content for keyword in keywords):
            return extension_language

    # Extension unknown, or its keyword check failed — score everything
    best_language = "Unknown"
    highest_score = 0

    for language, keywords in KEYWORD_HINTS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in content)
        if score > highest_score:
            highest_score = score
            best_language = language

    return best_language

