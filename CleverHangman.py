'''
Description:
        You must create a Hangman game that allows the user to play and guess a secret word.  
        See the assignment description for details.
    
@author: Patrick Lee   pyl7
'''

import random

DEBUG = False

def handleUserInputDifficulty():
    ''' 
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the 
    corresponding number of misses allowed for the game. 
    '''
    
    print("you'll get 12 misses unless you enter 'h' for 'hard to guess'")
    print("How many misses do you want? Hard has 8 and Easy has 12")
    letterChosen = input('(h)ard or (e)asy> ')
    if letterChosen == 'h':
        return 8
    elif letterChosen == 'e':
        return 12

def getWord(words, length):
    '''
    Selects the secret word that the user must guess. 
    This is done by randomly selecting a word from words that is of length length.
    '''
    newList = []
    for word in words:
        word = word[:-1]
        if len(word) == int(length):
            newList.append(word)
    randomPosition = random.randrange(0, len(newList), 1)
    return newList[randomPosition]

def createDisplayString(lettersGuessed, misses, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    printedalphabet = list(alphabet)
    lettersGuessed.sort() #lettersGuessed is a list
    for theletter in lettersGuessed:
        if theletter in printedalphabet:
            theposition = printedalphabet.index(theletter)
            printedalphabet[theposition] = " "
    lettersGuessedValue = ""
    for char in printedalphabet:
        lettersGuessedValue = lettersGuessedValue + char
    lettersGuessedValue = lettersGuessedValue.rstrip()
    hangmanWordValue = ""
    for char in hangmanWord:
        hangmanWordValue = hangmanWordValue + char + " "
    hangmanWordValue = hangmanWordValue.rstrip()
    message_old = "letters you've guessed:  "
    message = "letters not yet guessed: "
    message2 = "misses remaining = "
    return message + lettersGuessedValue + "\n" + message2 + str(misses) + "\n" + hangmanWordValue

def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    
    something = False
    while not something:
        print(displayString)
        inputValue = input("letter> ")
        if inputValue not in lettersGuessed:
            something = True
            return inputValue
        elif inputValue in lettersGuessed:
            print("you already guessed that")

def updateHangmanWord(guessedLetter, secretWord, hangmanWord):
    '''
    Updates hangmanWord according to whether guessedLetter is in secretWord and where in secretWord guessedLetter is in.
    '''
    
    positionsList = []
    if guessedLetter in secretWord:
        for x in range(len(secretWord)):
            if guessedLetter == secretWord[x]:
                positionsList.append(x)
    elif guessedLetter not in secretWord:
        return hangmanWord
    
    for number in positionsList:
        hangmanWord[number] = guessedLetter
    
    return hangmanWord

def processUserGuess(guessedLetter, secretWord, hangmanWord, misses):
    '''
    Uses the information in the parameters to update the user's progress in the hangman game.
    '''
    
    newList = [updateHangmanWord(guessedLetter, secretWord, hangmanWord), misses, True]    
    return newList

def handleUserInputDebugMode():
    ''' 
    This function asks the user if they would like to play in debug mode or not.
    True is returned if the user enters 'd', and False is returned otherwise.
    '''
    
    letterChosen = input('Which mode do you want: (d)ebug or (p)lay: ')
    if str(letterChosen) == 'd':
        return True
    else:
        return False

def handleUserInputWordLength():
    ''' 
    This function asks the user what length secretWord should be, 
    then returns the corresponding length.
    '''
    
    numberOfLetters = input("How many letters in the word you'll guess: ")
    return int(numberOfLetters)

def createTemplate(currentTemplate, letterGuess, word):
    """
    This function creates and returns a new template.
    The new template should be consistent with word and the new letterGuess.
    """
    
    newTemplate = list(currentTemplate)
    if letterGuess in word and word.count(letterGuess) == 1:
        position = word.index(letterGuess)
        newTemplate[position] = letterGuess
        finalTemplate = "".join(newTemplate)
        return finalTemplate
    elif letterGuess in word and word.count(letterGuess) > 1:
        listOfPositions = [i for i, letter in enumerate(word) if letter == letterGuess]
        for position in listOfPositions:
            newTemplate[position] = letterGuess
        finalTemplate = "".join(newTemplate)
        return finalTemplate
    else:
        return "".join(currentTemplate)

def getNewWordList(currentTemplate, letterGuess, wordList):
    """
    This function creates a dictionary where the values are a list of words.
    The key for each list is the string returned by createTemplete() for those words.
    The longest list in the dictionary and its corresponding template is returned.
    """
    
    thedict = {}
    for word in wordList:
        if len(word) != len(currentTemplate): continue
        modifiedTemplate = createTemplate(currentTemplate, letterGuess, word)
        #print(modifiedTemplate)
        if modifiedTemplate not in thedict:
            thedict[modifiedTemplate] = []
        thedict[modifiedTemplate].append(word)
    # Find the longest one and return it in the two-tuple form
    listOfTuples = thedict.items()
    # print(listOfTuples)
    listOfLengths = []
    for element in listOfTuples:
        listOfLengths.append((element[0], len(element[1]), element[1]))
    listOfLengths = sorted(listOfLengths, reverse = False, key = lambda element: (element[0]))
    if DEBUG == True:
        for element in listOfLengths:
            print(element[0] + " : " + str(len(element[2])))
        print("# keys = " + str(len(listOfTuples)))
    listOfLengths = sorted(listOfLengths, reverse = True, key = lambda element: (element[1]))
    finalTuple = (listOfLengths[0][0], listOfLengths[0][2])
    return finalTuple
    
def returnLettersAlreadyGuessed(lettersAlreadyGuessed):
    """
    This function returns the argument provided, letters already guessed.
    """
    return lettersAlreadyGuessed

def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''
    
    file = open(filename, "r")
    lengthOfSecretWord = random.randrange(5, 11)
    listOfWords = file.readlines()
    file.close()
    
    global DEBUG
    DEBUG = handleUserInputDebugMode()
    wordLength = handleUserInputWordLength()
    
    file = open(filename, "r")
    listOfWords = file.read().splitlines()
    file.close()
    
    missesRemaining = handleUserInputDifficulty()
    numberOfMisses = missesRemaining
    hangmanWord = getWord(listOfWords, wordLength)
    currentHangmanWord = []

    for x in range(len(hangmanWord)):
        currentHangmanWord.append('_')

    lettersGuessed = []
    theTuple = ''

    runningList = listOfWords
    
    while '_' in currentHangmanWord:
        if DEBUG == True:
            print('(word is ' + hangmanWord + ')')
            print('# possible words: ' + str(len(listOfWords)))
        guessedLetterNotAlreadyGuessed = handleUserInputLetterGuess(lettersGuessed, createDisplayString(lettersGuessed, missesRemaining, currentHangmanWord))
        lettersGuessed.append(guessedLetterNotAlreadyGuessed)

        theTuple = getNewWordList(currentHangmanWord, guessedLetterNotAlreadyGuessed, runningList)
        runningList = theTuple[1]
        
        listOfWords = theTuple[1]
        
        randomPosition1 = random.randrange(0,len(theTuple[1]),1)

        hangmanWord = theTuple[1][randomPosition1]
        processUserGuess(guessedLetterNotAlreadyGuessed, hangmanWord, currentHangmanWord, missesRemaining)
        
        if guessedLetterNotAlreadyGuessed not in hangmanWord:
            print("you missed: " + guessedLetterNotAlreadyGuessed + " not in word")
            missesRemaining = missesRemaining - 1

        if missesRemaining == 0:
            print("you're hung!!" + "\n" + "word was " + hangmanWord + "\n" + "you made " + str(len(lettersGuessed)) + " guesses with " + str(numberOfMisses - missesRemaining) + " misses")
            return False

    if '_' not in currentHangmanWord:
        print("you guessed the word: " + hangmanWord + "\n" + "you made " + str(len(lettersGuessed)) + " guesses with " + str(numberOfMisses - missesRemaining) + " misses" )
        return True

if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    runGame("lowerwords.txt")
