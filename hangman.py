from AH import Ascii_Hangman
from colorama import Back
import sys
import time

#I use sys.stdout write and flush a lot
#I know that print() is the same as sys.stdout.write()
#but i think being consistent is nicer (use sys.stdout for both)

def hangman(word, guesses, padding=0):
    top_info = 'Guesses allowed: %s\nWord: %s (%s)\n' % (guesses, '*'*len(word), len(word))

    h = Ascii_Hangman(guesses, padding)
    hangman_string = h.current
    guessed_set = set([])
    word_set = set(word)
    alpha_set = set('abcdefghijklmnopqrstuvwxyz')
    current_output = ''

    new_reminder = False
    valid_reminder = False
    single_reminder = False

    #initial screen draw
    guess_line = ''
    for char in word:
        guess_line += '_ '
    guess_line = guess_line[:-1]
    output = '\033[2J\033[H'+top_info+'\n'+hangman_string+'\n\n'
    output += ' '*padding + guess_line
    output += '\n\nGuessed: '+' '.join(guessed_set)
    output += '\nLives left: %s\n\n' % guesses
    sys.stdout.write(output)
    sys.stdout.flush()
    current_output = output


    while guessed_set != word_set:
        if new_reminder:
            char = input('Enter a NEW character: ')
        elif valid_reminder:
            char = input('Enter a VALID character (a-z): ')
        elif single_reminder:
            char = input('Enter a SINGLE character: ')
        else:
            char = input('Enter a character: ')

        new_reminder = False
        valid_reminder = False
        single_reminder = False

        if char in guessed_set:
            #flash_screen('yellow')
            new_reminder = True
            print(Back.YELLOW)
            sys.stdout.write(current_output)
            sys.stdout.flush()
            time.sleep(0.05)
            print(Back.RESET)
            sys.stdout.write(current_output)
            sys.stdout.flush()
            #sys.stdout.write('\033[F\033[K')
            continue
        elif len(char) != 1:
            #flash_screen('yellow')
            single_reminder = True
            print(Back.YELLOW)
            sys.stdout.write(current_output)
            sys.stdout.flush()
            time.sleep(0.05)
            print(Back.RESET)
            sys.stdout.write(current_output)
            sys.stdout.flush()
            sys.stdout.write('\033[F\033[K')
            continue
        elif char not in alpha_set:
            #flash_screen('yellow')
            valid_reminder = True
            print(Back.YELLOW)
            sys.stdout.write(current_output)
            sys.stdout.flush()
            time.sleep(0.05)
            print(Back.RESET)
            sys.stdout.write(current_output)
            sys.stdout.flush()
            sys.stdout.write('\033[F\033[K')
            continue

        if char in word_set:
            print(Back.GREEN)
            sys.stdout.write(current_output)
            sys.stdout.flush()
            time.sleep(0.05)
            guessed_set.add(char)
            guess_line = ''
            for char in word:
                if char in guessed_set:
                    guess_line += char+' '
                else:
                    guess_line += '_ '
            guess_line = ' '*padding + guess_line[:-1]
            output = '\033[2J\033[H'+top_info+'\n'+hangman_string+'\n\n'+guess_line
            g = list(guessed_set)
            g.sort()
            output += '\n\nGuessed: '+' '.join(g)
            output += '\nLives left: %s\n\n' % guesses

        else:
            print(Back.RED)
            sys.stdout.write(current_output)
            sys.stdout.flush()
            time.sleep(0.05)
            guessed_set.add(char)
            guesses -= 1
            guess_line = ''
            for char in word:
                if char in guessed_set:
                    guess_line += char+' '
                else:
                    guess_line += '_ '
            guess_line = ' '*padding + guess_line[:-1]
            hangman_string = h.next()
            if hangman_string == None:
                break
            output = '\033[2J\033[H'+top_info+'\n'+hangman_string+'\n\n'+guess_line
            g = list(guessed_set)
            g.sort()
            output += '\n\nGuessed: '+' '.join(g)
            output += '\nLives left: %s\n\n' % guesses

        print(Back.RESET)
        sys.stdout.write(output)
        sys.stdout.flush()
        current_output = output

    output = '\033[2J\033[H%s\n%s\n' % (top_info, h.end)
    print(Back.RESET)
    sys.stdout.write(output)
    sys.stdout.flush()



if __name__ == '__main__':
    sys.stdout.write('\033[2J\033[H') #put 3 if u wanna be a dick and clear scrollback buffer
    sys.stdout.flush()

    print('Guesses allowed must be between 1 and 12 inclusive.')
    guesses = input('Guesses allowed: ')
    if len(guesses) == 0:
        guesses = 12 #max
    else:
        guesses = int(guesses)
    assert(0 < guesses < 13), 'Guess is out of allowed range.'

    sys.stdout.write('\033[2F\033[2K\033[S\033[E')
    sys.stdout.flush()

    print('Word length must be between 1 and 20 inclusive, and be comprised of letters (whitespace will be removed).')
    word = input('Word: ')
    word = word.lower()
    words = word.split()
    word = ''.join(words)
    assert(0 < len(word) < 21), 'Word length is out of the allowed range.'
    assert(set(word).issubset(set('abcdefghijklmnopqrstuvwxyz '))), 'Invalid characters used.'

    sys.stdout.write('\033[2F\033[2K \bGuesses allowed: %s\033[S\033[2K\003[G' % guesses)
    sys.stdout.flush()
    print('Word:', '*'*len(word), '(%s)' % len(word))

    hangman(word, guesses, padding=4)
