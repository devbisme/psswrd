# psswrd

Simple script with a GUI that generates pronounceable passwords and places them on the clipboard.


## Description

I always have to make passwords and answer security questions.
This script makes it easy to create random text strings and paste them into forms.

## Installation

Install `psswrd` as follows:

```bash
pip install psswrd
```

## Usage

Use `psswrd` as follows:

1. Start the GUI.
2. A random password will appear in the `Password` field. It will also be copied onto the clipboard.
3. If you like the password, press `Done` and `psswrd` will close.
4. If you don't like the password, press `Again` and another password will appear and be copied onto the clipboard.
5. If there are restrictions on allowable passwords, you can specify a format in the `Template` field using the following characters:
   1. `l` stands for a random lowercase letter from `a-z`.
   2. `u` stands for a random uppercase letter from `A-Z`.
   3. `m` stands for a random mixed-case letter from `A-Za-z`.
   4. `d` stands for a random digit from `0-9`.
   5. `p` stands for a random punctuation character from `!@#$%&*+-=?;`.
   6. Any other character is copied directly into the password.

## FAQ

### Why do you say the passwords are pronounceable?

The letters A-Z are randomly selected such that they follow a probability distribution based on trigrams
extracted from a corpus of text. So the strings of letters kind of look like words and are often
pronounceable although it's not guaranteed.

### What text is used for the corpus?

The probability distribution of letter trigrams was generated from the text of the short story ["Day of the Comet"](https://www.gutenberg.org/ebooks/65726) found on Project Gutenberg.
