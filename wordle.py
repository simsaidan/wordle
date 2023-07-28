import random
from urllib import response
from colorama import init, Fore
from bs4 import BeautifulSoup
import requests
import sqlite3
import pytest

conn = sqlite3.connect("wordle.sqlite")
cur = conn.cursor()

init()

words = cur.execute("SELECT * FROM wordle").fetchall()
word = random.choice(words)[0].upper()


def valid_word(word):
    """This function checks to see if a word is valid, by first looking it up
    in SQLite database. If not found, it'll try to access the website to check.
    """

    assert len(word) == 5
    found = cur.execute("SELECT * FROM wordle WHERE words = ?", (word.lower(),))
    if found.fetchone():
        return True
    link = "https://www.dictionary.com/browse/" + word
    response = requests.get(link)
    soup = BeautifulSoup(response.content, features="lxml")
    spans = soup.find_all("span")
    for span in spans:
        if "no-results" in str(span) or "No results" in str(span):
            return False
    cur.execute("INSERT INTO wordle (words) VALUES (?)", (word.lower(),))
    conn.commit()
    return True


def not_rest_same(g, w, index, letter):
    """not_rest_same(guess, word, index, letter) checks whether the
    letter does not appear in the rest of guess, or appears at a different
    position from the rest of word."""
    w = w[:index] + w[index + 1 :]
    g = g[:index] + g[index + 1 :]
    if letter not in g:
        return True
    for i in range(len(g)):
        if g[i] == letter and g[i] != w[i]:
            return True  # yellow return False # dark


def colors(g, w, index):
    """colors(guess, word, ix) returns different colors depending on whether
    the ith letter of guess matches the ith letter of word, or doesn't match but
    appears in word.

    Precondition: guess and word are uppercase strings.
    Precondition: index is an int in 0 through 4, inclusive"""
    if g[index] == w[index]:
        return Fore.GREEN
    if g[index] in w and not_rest_same(g, w, index, g[index]):
        return Fore.YELLOW
    return Fore.RESET


guess_index = ["first", "second", "third", "fourth", "fifth", "sixth"]


def main():
    print("Welcome to PyWordle!")
    guesses = 0
    while guesses < 6:
        valid = False
        while not valid:
            guess = input("What is your " + guess_index[guesses] + " guess: ").upper()
            if len(guess) == 5 and valid_word(guess):
                valid = True
            else:
                print("That is not a valid 5 letter word")
        if guess == word:
            print(Fore.GREEN + "Congrats! You win!")
            quit()
        print(
            colors(guess, word, 0)
            + guess[0]
            + colors(guess, word, 1)
            + guess[1]
            + colors(guess, word, 2)
            + guess[2]
            + colors(guess, word, 3)
            + guess[3]
            + colors(guess, word, 4)
            + guess[4]
            + Fore.RESET
        )
        guesses += 1
    print(Fore.RED + "Sorry. You lose. The word was " + word + ".")
    quit()


if __name__ == "__main__":
    main()
