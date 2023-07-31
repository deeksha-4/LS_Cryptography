import itertools, re

text=input()
text=text.upper()
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SILENT_MODE = False # If set to True, program doesn't print anything.
MAX_KEY_LENGTH = 12 # Will not attempt keys longer than this.
NONLETTERS_PATTERN = re.compile('[^A-Z]')
#Storing alphabets in decreasing order of frequency in normal English text
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
#Storing in normal order
LETTERS_AND_SPACE = LETTERS + ' \t\n'

def getLetterCount(message):
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1

    return letterCount


def getItemAtIndexZero(items):
    return items[0]


def getFrequencyOrder(message):
    letterToFreq = getLetterCount(message)
    freqToLetter = {}
    for letter in LETTERS:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)
    for freq in freqToLetter:
        freqToLetter[freq].sort(key=ETAOIN.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=getItemAtIndexZero, reverse=True)
    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)

def englishFreqMatchScore(message):
    freqOrder = getFrequencyOrder(message)
    matchScore = 0
    for commonLetter in ETAOIN[:6]:
        if commonLetter in freqOrder[:6]:
            matchScore += 1
    for uncommonLetter in ETAOIN[-6:]:
        if uncommonLetter in freqOrder[-6:]:
            matchScore += 1
    return matchScore

def loadDictionary():
    dictionaryFile = open('dictionary.txt')
    englishWords = {}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word] = None
    dictionaryFile.close()
    return englishWords

ENGLISH_WORDS = loadDictionary()

def getEnglishCount(message):
    message = message.upper()
    message = removeNonLetters(message)
    possibleWords = message.split()

    if possibleWords == []:
        return 0.0 # No words at all, so return 0.0.

    matches = 0
    for word in possibleWords:
        if word in ENGLISH_WORDS:
            matches += 1
    return float(matches) / len(possibleWords)


def removeNonLetters(message):
    lettersOnly = []
    for symbol in message:
        if symbol in LETTERS_AND_SPACE:
            lettersOnly.append(symbol)
    return ''.join(lettersOnly)


def isEnglish(message, wordPercentage=20, letterPercentage=85):
    wordsMatch = getEnglishCount(message) * 100 >= wordPercentage
    numLetters = len(removeNonLetters(message))
    messageLettersPercentage = float(numLetters) / len(message) * 100
    lettersMatch = messageLettersPercentage >= letterPercentage
    return wordsMatch and lettersMatch

def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')

def translateMessage(key, message, mode):
    translated = []

    keyIndex = 0
    key = key.upper()

    for symbol in message: 
        num = LETTERS.find(symbol.upper())
        if num != -1:
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) 
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) 
            num %= len(LETTERS) 
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
            keyIndex += 1 # Move to the next letter in the key.
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Append the symbol without encrypting/decrypting.
            translated.append(symbol)
    return ''.join(translated)

def findRepeatSequencesSpacings(message):
    message = NONLETTERS_PATTERN.sub('', message.upper())
    seqSpacings = {} 
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart + seqLen]
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] 
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getUsefulFactors(num):
    if num < 2:
        return []
    factors = [] 
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)
            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors)) 
    
def getItemAtIndexOne(items):
    return items[1]

def getMostCommonFactors(seqFactors):
    factorCounts = {}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1
    factorsByCount = []
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH:
            factorsByCount.append( (factor, factorCounts[factor]) )
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)
    return factorsByCount

def kasiskiExamination(ciphertext):
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))
    factorsByCount = getMostCommonFactors(seqFactors)
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])
    return allLikelyKeyLengths


def getNthSubkeysLetters(nth, keyLength, message):
    message = NONLETTERS_PATTERN.sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    ciphertextUp = ciphertext.upper()
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)
        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        freqScores.sort(key=getItemAtIndexOne, reverse=True)
        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print() # Print a newline.
            
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]

        decryptedText = decryptMessage(possibleKey, ciphertextUp)

        if isEnglish(decryptedText):
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)

            # Check with user to see if the key has been found:
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText) # Only show first 200 characters.
            print()
            print('Enter D if done, anything else to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return  possibleKey, decryptedText

    # No English-looking decryption found, so return None:
    return None


def hackVigenere(ciphertext):
    # First, we need to do Kasiski Examination to figure out what the
    # length of the ciphertext's encryption key is:
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Kasiski Examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            break

    # If none of the key lengths we found using Kasiski Examination
    # worked, start brute-forcing through key lengths:
    if hackedMessage == None:
        if not SILENT_MODE:
            print('Unable to hack message with likely key length(s). Brute forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # Don't re-check key lengths already tried from Kasiski:
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage != None:
                    break
    return hackedMessage

NUM_MOST_FREQ_LETTERS = 3 # Attempt 4 letters per subkey.
hackedMessage = hackVigenere(text)

if hackedMessage != None:
    print(f'Plain text= ',hackedMessage[1],'\n', 'Key= ', hackedMessage[0])
else:
    print('Failed to hack encryption.')
