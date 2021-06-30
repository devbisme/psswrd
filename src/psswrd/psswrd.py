#!/usr/bin/env python

# MIT license. Copyright 2021 by Dave Vandenbout.

import argparse
import sys
import re
from collections import defaultdict, Counter
from random import choice, choices
import pyperclip

import PySimpleGUI as sg

from psswrd import __version__

__author__ = "Dave Vandenbout"
__copyright__ = "Dave Vandenbout"
__license__ = "MIT"

gui_font = "Consolas 15"
# sg.theme('DarkAmber')


def show_msg(msg):
    """Show message in dialog box with OK button to dismiss."""

    event, values = sg.Window(
        "pwd",
        [
            [sg.Text(msg, font=gui_font)],
            [sg.Submit("OK", font=gui_font)],
        ],
    ).read(close=True)


class Ngram:
    """Generates N-gram statistics from a corpus of text."""

    def __init__(self, corpus, n):
        """Generates N-gram statistics from a corpus of text.

        Args:
            corpus (string): Corpus of text from which N-gram probabilities are extracted.
            n (integer): Length of N-grams.
        """
        table = defaultdict(Counter)
        for i in range(0, len(corpus) - n):
            pre = corpus[i : i + n]
            nxt = corpus[i + n]
            while pre:
                table[pre][nxt] += 1
                pre = pre[1:]
        self.table = dict(table)
        self.n = n

    def __getitem__(self, pre):
        """Given a prefix string, return the next character as weighted by N-gram probabilities.

        Args:
            pre (string): Prefix string used for lookup into N-gram table.

        Returns:
            character: Character that follows the prefix with selection weighted by N-gram probabilities.
        """
        table = self.table
        pre = pre[-self.n :]
        while pre:
            try:
                ctr = table[pre]
                return choices(list(ctr.keys()), weights=ctr.values())[0]
            except KeyError:
                pre = pre[1:]
        ctr = table[choice(list(table.keys()))]
        return choices(list(ctr.keys()), weights=ctr.values())[0]

    def phrase(self, length):
        """Return a phrase of a selected length with letter frequencies that mirror the corpus.

        Args:
            length (integer): Length of phrase to generate.

        Returns:
            string: Generated phrase.
        """
        s = ""
        for _ in range(length):
            s += self[s]
        return s


def generate_password(ngram, template):
    """Generate a password given an N-gram table and a template.

    Args:
        ngram (Ngram): N-gram table.
        template (string): Password template.

    Returns:
        string: The generated password.
    """

    pwd_len = len(template)
    phrase = list(ngram.phrase(pwd_len))  # Random string with N-gram statistics.
    phrase.reverse()  # So we can use pop() to extract letters in order.

    pwd = []  # Empty password.

    for c in template:
        if c == "u":
            # Add next letter from phrase and uppercase it.
            pwd.append(phrase.pop().upper())
        elif c == "l":
            # Add next letter from phrase and lowercase it.
            pwd.append(phrase.pop())
        elif c == "m":
            # Add next letter from phrase and randomly choose to upper or lowercase it.
            pc = phrase.pop()
            pwd.append(choice([pc.lower(), pc.upper()]))
        elif c == "d":
            # Add a random digit.
            pwd.append(choice("0123456789"))
        elif c == "p":
            # Add a random punctuation mark.
            pwd.append(choice(r"!@#$%&*+-=?;"))
        else:
            # Add the character from the template.
            pwd.append(c)

    # Join password characters into a string and return it.
    return "".join(pwd)


def password_gui(ngram):
    """Password GUI

    Args:
        ngram (Ngram): N-gram table.
    """

    # Default password template.
    template = "llllllllddd"

    # Create GUI window with the specified layout.
    layout = [
        [
            sg.Text("Password:", font=gui_font),
            sg.InputText(key="-PWD-", size=(38, 1), font=gui_font),
        ],
        [
            sg.Submit("Again", font=gui_font),
            sg.Cancel("Done", font=gui_font),
            sg.Text("   "),
            sg.Text("Template:", font=gui_font),
            sg.InputText(default_text=template, size=(20, 1), font=gui_font),
        ],
    ]
    window = sg.Window("psswrd - Generate a Password", layout, finalize=True)

    # Repetitively generate passwords until Done is clicked.
    while True:

        # Generate password, copy it to clipboard, and display it in GUI.
        password = generate_password(ngram, template)
        pyperclip.copy(password)
        window["-PWD-"].update(password)

        # Wait for user to click a button.
        event, values = window.read()

        # Exit if the Done button is clicked.
        if event in (sg.WIN_CLOSED, "Done"):
            window.close()
            sys.exit(0)

        # Get the template in case the user changed it.
        _, template = values.values()


def parse_args():
    """Parse command line parameters."""

    parser = argparse.ArgumentParser(
        description="pwd for generating pronounceable passwords."
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="pwd {ver}".format(ver=__version__),
    )

    return parser.parse_args()


def main():
    args = parse_args()

    corpus = re.sub(r"[\W\d]", "", corpus_text).lower()

    ngram = Ngram(corpus, 3)

    password_gui(ngram)


if __name__ == "__main__":
    main()


corpus_text = """
               When the world you live on is about to be
            destroyed in a matter of hours, petty squabbles
           no longer seem important; only Time--and regret!

           [Transcriber's Note: This etext was produced from
              Imagination Stories of Science and Fantasy
                             October 1956
         Extensive research did not uncover any evidence that
         the U.S. copyright on this publication was renewed.]


So far as the public was concerned, the comet was discovered at 10:00
a.m. on a Friday morning; just when Frank and Dee Allison were in the
midst of their bitterest domestic quarrel. Dee had just spoken through
clenched teeth:

"I never knew I could hate a person the way I hate you."

"I consider that an honor!" Frank snapped back.

Then the music on the radio was cut off and the announcement was
made--in the calm, impersonal voice of the announcer that gave it a
flavor of grotesque unreality....

"--and so, although the discovery of the celestial interloper was made
by astronomers some time ago, the announcement was delayed until all
doubt as to its orbit had been dispelled. Thus, a direct and dismal
statement becomes a matter of necessity--the earth is doomed--"

Frank and Dee stared mutely at one another, trying to comprehend. "It's
some kind of a gag," Frank said.

Dee shook her head. "No--that was John Kalmus, the Green Network
commentator who cut in. He wouldn't be a party to any hoax."

Frank knew this of course, but the destruction of the world was a
pretty big lump to swallow in a matter of seconds. They continued
to stare at each other, taking the rest of the story into their
numbed minds. The end would come at exactly 1:42 on Sunday. Prior
to that time, there would be vast weather disturbances and tidal
catastrophies the world over. But these would be far milder than what
would ordinarily be expected because the comet was moving at such a
tremendous rate of speed. There would be no long-drawn out suffering.

"At least that's a blessing," Dee said.

"Uh-huh. Say--I'll bet the churches will be crowded."

"No doubt." Dee paused, and added, "How long since we've been to
church, Frank?"

       *       *       *       *       *

There had been a cabinet meeting and now the President of the United
States was seated alone in his study. He picked up his phone and asked,
"How about that call to the Kremlin? Why the delay?"

The operator said, "The Premier was busy on the phone--not taking any
calls, but it seems he was trying to get through to you. May I connect
him, sir?"

"By all means."

The normally harsh voice of the Russian Premier was oddly quiet and
pensive. "Mr. President?"

"Mr. Premier. I was trying to get through to you."

"They told me. How--how are things there? How are your people taking it
in the United States?"

"Very well. They are stunned, naturally, and I'm sure quite a few of
them don't believe it. It will take a little time."

The Russian Premier chuckled with a note of wistfulness. "That's
exactly what they will have--very little time."

"And your people--?"

"We haven't told them. We thought it best."

The President sighed. "We stick to our ideologies to the very end,
don't we?"

"Policy can't be changed overnight. Yet great strides can be made."

"I don't think I understand you."

"I'll try to clarify. We finished our public statement Monday, setting
down our position on The Stockholm Conference last month."

"The conference was a great disappointment to me--to you also, I
imagine."

"Yes, and our public statement was, well, pretty bleak, but I'm
changing it. I'm in the middle of rewriting it now."

"I'd like to sit down with you and perhaps readjust some of our own
demands."

"I'd like to have you."

"No time now, of course."

"No, in fact the rewriting may seem futile to you but it gives me great
satisfaction. A nice way to end a political career."

"Why don't you call me back and read it to me when you've finished?"

"I'll do that. Goodbye Mr. President."

       *       *       *       *       *

Frank and Dee Allison walked hand in hand down the street. Dee had been
crying but now her tears had been dried and her expression was calm.
There was a wistful light in her eyes. "It could have been so much
different, Frank."

"Yes darling. My fault. It was my damn temper."

"But I was always ready to snarl back. A wife's job is to--"

He squeezed her hand. "Are you afraid, baby?"

"No--no. I won't be afraid as long as you're there to hold my hand."

He put his arm around her shoulders and drew her close and they walked
with the other people toward the Church.

       *       *       *       *       *

The President of the United States put through a call to the Premier
of Russia. Connections clicked into place across half a world and the
Russian operator's voice came through warm and cordial. "Of course, Mr.
President. The Premier's wire is always open to you. I'll ring him."

The phone was lifted instantly. "Mr. President! How nice of you to
call!"

"Our previous conversation set me thinking, Mr. Premier. I want to be a
part of your inspiring idea. So I'm rewriting our own statement and I
suggest we make a joint public release. I think it will help the people
of the world to face the end with greater dignity. The _knowing_--I
think--will help."

"I'm sure it will. How soon will your draft be finished?"

"Can you give me another two hours?"

"Of course. Ring me when you're ready. Perhaps we can set up an
international television hookup and appear together."

"I'm sure we can."

       *       *       *       *       *

Frank and Dee Allison came out of church bringing some of the peace
and the strength with them. Dee said, "I'd like to see my mother for a
little while before--before--"

Frank nodded. "Of course. And I think you should drop in on her alone."

"Oh, no--I--"

"A goodbye like this one should be said alone. You go up. I'll give you
fifteen minutes and then call for you."

Dee's eyes were misty. "You're so understanding. Oh, why couldn't we
have--"

Frank grinned. "Come on, angel. Heads up. Eyes bright."

They walked up the street, others around them going quietly about their
business. The people were very calm.

       *       *       *       *       *

The conference of astronomers and scientists realized their ghastly
blunder at 11:59 a.m. For a long moment, there was stunned silence in
the room. None of them could believe that such a progressive series of
errors could have been passed from man to man and been added to by
each. Through every mind went the dread of what would come out of this.
In the future it would be called the greatest hoax of all time. There
would be gigantic investigations. Possibly a goat would have to be
found. The world would never believe the truth.

"We might as well make the announcement," someone said.

"You make it," another scientist said. "I'm leaving for the North Pole."

       *       *       *       *       *

Frank Allison heard the announcement from a loudspeaker in a store
window on his sixth trip around the block. He'd been walking slowly,
deep in his own thoughts and regrets--giving Dee a little more time
with her mother. Then--

"--so the great danger is passed, ladies and gentlemen. The why and
the wherefore of it is not known at this time. We are only sure of one
thing: The comet will swing away into space. Rumor has it that the size
of the invading body was what threw our scientists off. But whether
the earlier announcement was sincere or merely a cruel joke will not
be known immediately. The main thing is to be thankful that an error
existed--whatever its cause--"

Frank straightened his shoulders, turned and started briskly up the
street.

       *       *       *       *       *

The President of the United States put a call through to the Russian
Premier. He awaited expectantly with the phone in his hand. But the
connections slipped into place slowly and five minutes later a voice
came across half a world. "The Premier is busy. Please inform the
President of the United States that the Premier is engaged. Inform the
President that I am able to connect him with the Premier's secretary.
Ask him if that will be satisfactory."

The frost in the voice seemed to chill the President's ear. "I will
talk to the Premier's secretary."

The Secretary's voice was careful, guarded. "May I help you, Mr.
President?"

"Perhaps you can. I had a conversation with the Premier a little over
an hour ago. We were planning a joint statement--a joint television
appearance."

The secretary's voice stiffened. "I'm sorry, but I know of no such
statement nor of any such plans on the part of the Premier.'"

"May I speak to the Premier?"

"I'm sorry. The Premier has left on an extended vacation."

"I'm sorry too," the President said, and cradled the phone.

       *       *       *       *       *

Dee Allison sat tight-eyed staring out the window. Her handkerchief was
balled into a wad in her hand. "He's so cruel--so thoughtless," she
said.

Her mother regarded her with resignation. "What do you want me to tell
him when he comes?"

"Tell him I never want to see him again!"

       *       *       *       *       *

Frank Allison got as far as the lobby of the building in which Mrs.
Gregg, Dee's mother, lived. He raised his hand and his finger was
inches from the bell. Then he doubled the hand into a fist and thrust
it into his pocket. "The hell with it!" he growled. "If she wants to
see me, she knows where to find me." He turned and strode out of the
building.

       *       *       *       *       *

The President of the United States had sat staring into space for a
long time. A sound caused him to look up. His secretary stood by the
desk. "Yes?"

"This new statement you just prepared, Mr. President. I'm not entirely
clear on how you plan to use it--what should I do?"

"Tear it up," the President said wearily, "and throw it in the
wastebasket. Things are now back to normal."
"""
