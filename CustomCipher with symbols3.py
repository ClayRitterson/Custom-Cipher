# Custom Cipher with Extra Vignere Layer (Now with symbols!)
# Written by: CWR, 2022

# General Notes:
# This is not intended to be an truly secure encryption. Going forward I will
# attempt a more secure encryption by factoring large prime numbers. In this example
# If one knows the technique used to encrypt these methods, the cipher is only as secure as the
# Vignere Cipher. 

#********************************************************************************************************************************
# The program first takes an embedded keyword. It uses the index of the first char modulus length of keyword
# to determine the position of the keyword ceaser key, which is then removed from the keyword and used to perform a 
# Caesar shift. Then it adds a character to the start to indicate keyword length. 

# The counts and removes spaces, and then represents the the index of each space by using two letters
# For example, 'aa' represents a space at index 0, 'ab' represents a space at index 1, and so on. Also adds
# two letters to the end to indicate number of spaces to be read

# Both of these codes and then futher encrypted using a non-caesar shift, by shifting each char by the
# len of the chunk of each code by it's index in that chunk.

# The modified keyword is then used to perform a vignere cipher on the main body of text, and then
# the keyword is added to the front of the text, and the spaces code is added to the end.

# Next, the program shuffles the entire string by running the jospehus problem over and over, placing
# Placing the strings in the order that each would "win" the josephus problem, until the entire string has
# Been shuffled

# Next, the user is prompted for an additional keyword to perform a final vignere cipher. This keyword is not embedded
# but must be known by the recipient, otherwise someone who knows the steps could decrypt without a keyword

# To decrypt, each step is performed in a reverse order until the original text remains.
#********************************************************************************************************************************

#Menu options
# 1. Encrypt Text
# 2. Decrypt Text
# 3. Encrypt and Decrypt Text
# 4. Quit Program

# How to use
# First, enter a plain text messege that contains only letters and spaces, and is 600 chars or less including spaces
# Second, enter an embedded keyword that is between 5 and 20 chars and only contains letters 
# Third, pick another keyword of the same contraints, this keyword will not be embedded in the encrypted text and must be known
# by the person receving the messege in order to decipher
# Finally, re-enter the second keyword to decipher the messege

# Test the program's validity
# To prove the program really decrypts the encrypted string without saving any extra info, test it by encrypting a messege,
# copying the messege and the keyword, then close the program
# restart the program and decrypt the copied text

# List known bugs here:

#SAMPLE ENCRYPTIONS (Using menu option 2, enter encrypted text and then enter keyword )
#--------------------------------------------------------------------------------------------------------------------------------------
# -Kx9svKL*qEVIDtzi7ZK@fKEoNxr)zuq"x2JQVEDzG]^R
# Keyword: python
# 4sC4uy%sP:yM]dNx{q+eE7eI^jx/rG8aE9fN>qA7sE0qw6r%Q9wY;91iN[zQ3jI6mt%6M_HJ^mB*lE"pH6av^fm;plchy7mG3hj/vM9rK&guI6-?{q'vkSgKsnL@vq;jo={D*rn9wq/qC+jB+}A6uN)ep1E#]eC'lC&wJ'_J5ox4hq;}C8/v.5r?fw/dfKmGh9_!vNfahHoC3<A9my(eE/fC@gx5uP<dz]kz5vB@#]>oB5lu@mp8yQ%eI8uH<}JN&Yxuq^E{$c"v5y0I*Va;z5u]S-.m;p1z7M^$q;l3I7Tc$g)q"D6Sh$c=A'L_S>Xh.u:J{S_!r&C9J]O{Ul%A#J8QiVt?A3F#LcTr4B?I+v*eC?cBzcxarI7kw(rO]dG'_9gzByiqzRywyivpvrfExJiyAE@t{qkquumGw4gDChsIxvmnnnqtBnjE/pKn?p,tknnDHni'GrslxvkkoltDHJpmEuHC/hou(s$1AB9FDgJwlimvvjtIHl#gGu$yDiAZoNN'yDN?}fIZ?-qLX4/AY;8nI!gH.7fxN+9m%5/rW+}yPX2eC(]tQ,wrzjEHGgxzalvqrFxCxxGnpwl04mmELGahkdyIto<inCo3vpcnpcKzqBkktll5NwinrsPxpimwpxm!4rN#F1z;iP^(n"{Xs(cXgFe$hgpzuDxzxBgtE(KlyqAsxiy;rnhkFuEJ*vmB0Af7}3VLBBXGOyoArAgDJyslpzKDDwAEftimNg,*_;LnA3v1g-iurc2knnAn]3xp;Ab
# Keyword: champlaincollege
#--------------------------------------------------------------------------------------------------------------------------------------

#Game Control and Input Functions
#--------------------------------------------------------------------------------------------------------------------------------------
def menu():
    game = True
    while game == True:
        validOptions = ['1','2','3','4']
        validIn = False
        while validIn == False:
            select = str(input("SELECT MENU OPTION: "))
            if select not in validOptions:
                print("INVALID INPUT")
            else:
                break
        if select == '1':
            scrambledText = allEn()
            enVig = vignere(scrambledText, 'E')
            printMSG(enVig)
        elif select == '2':
            userScram = inputScrambled()
            allDe(userScram)
        elif select == '3':
            scrambledText = allEn() 
            enVig = vignere(scrambledText, 'E')    
            printMSG(enVig)       
            allDe(enVig)
        elif select == '4':
            break

def getKeyword(type):
    valid = False
    while valid == False:
        print("Enter ", type, end="")
        keyword = str(input(" keyword: "))
        stillValid = True
        for i in range(len(keyword)):
            if keyword[i] not in alph:
                stillValid = False
            if keyword[i] == ' ':
                stillValid = False
        if stillValid == False:
            print("Invalid Input: Unsupported Character")
        else:
            if len(keyword) < 5 or len(keyword) > 25:
                print("Keyword must be between 5 and 25 letters long")
            else:
                valid = True
    return keyword

def getPlainText():
    valid = False
    while valid == False:
        newText = ''
        plainText = str(input("Enter the message to encrypt: "))
        stillValid = True
        for i in range(len(plainText)):
            if plainText[i] not in alph:
                stillValid == False
        if stillValid == False:
            print("Invalid Input: Unsupported Character")
        else:
            for i in range(len(plainText)):
                if plainText[i] != ' ':
                    newText += plainText[i]
            if len(newText) > 8000:
                print("Message must be 8,000 characters or less, including spaces")
                print("Message is currently ", len(newText), " characters long")
            else:
                valid = True
    return plainText

def inputScrambled():
    validScram = False
    while validScram == False:
        inputScram = str(input("ENTER ENCRYPTED TEXT: "))
        if len(inputScram) > 0:
            validScram = True
        else:
            print("INVALID INPUT")
    return inputScram

#Decrypts Keyword using Caesar Cypher
#Location of Caesar Key determined by the the Index value of the first letter in the keyword, mod (length of keyword minus 1)
#The Caesar Key is then removed from the keyword, and the shift is applied
#--------------------------------------------------------------------------------------------------------------------------------------
def decrpytKey(keyword):
    keywordList = []
    for i in range(len(keyword)):
        keywordList.append(keyword[i])
    caesarKeyLocation = keywordList.pop(0)
    keyLocIndex = alph.index(caesarKeyLocation)
    keyLocInKey = keyLocIndex % (len(keyword) - 1)
    caesarKey = keywordList.pop(keyLocInKey)
    shiftKey = alph.index(caesarKey) + 1
    finalKeyword = ''
    for i in range(len(keywordList)):
        listVal = keywordList[i]
        listValIndex = alph.index(listVal)
        newValIndex = (listValIndex + (shiftKey * -1)) % 90
        newVal = alph[newValIndex]
        finalKeyword += newVal
    return(finalKeyword)

#Finds all of the Spaces in the initial Plain Text Message
#--------------------------------------------------------------------------------------------------------------------------------------
def findSpaces(plainText):
    spacesAt = []
    spacesFound = 0
    newText = ''
    for i in range(len(plainText)):
        if plainText[i] == ' ':
            spacesAt.append(i - spacesFound)
            spacesFound += 1
        else:
            newText += plainText[i]
    return newText, spacesAt

#Encrypts the list of spaces Indicies into a string of letters than can later be deciphered
#--------------------------------------------------------------------------------------------------------------------------------------
def encryptSpaces(spacesAt):
    if len(spacesAt) == 0:
        return 'ZZZ'
    crpytSpaces = ''
    newSpaces = ''
    for i in range(len(spacesAt)):
        spaceVal = spacesAt[i]
        spacer = (spaceVal // 90)
        spaceMod = spaceVal % 90
        spacerLetter = alph[spacer]
        spaceModLetter = alph[spaceMod]
        crpytSpaces += spacerLetter
        crpytSpaces += spaceModLetter
    for i in range(len(crpytSpaces)):
        newSpaces += crpytSpaces[len(crpytSpaces)-(i + 1)]
    cryptSpacer = (len(spacesAt) // 90)
    cryptMod = (len(spacesAt) % 90 )
    cryptSpacerLetter = alph[cryptSpacer]
    cryptModSpacer = alph[cryptMod]
    newSpaces += cryptModSpacer
    newSpaces += cryptSpacerLetter
    return newSpaces

#Performs a non-caesar shift on the string of space letters so they do not produce a pattern in the scrambled text
#--------------------------------------------------------------------------------------------------------------------------------------
def shiftSpaces(spaceAdd):
    shiftedSpace = ''
    endSpace = spaceAdd[len(spaceAdd)-2] + spaceAdd[len(spaceAdd) - 1]
    for i in range(len(spaceAdd)-2):
        newIndex = (alph.index(spaceAdd[i]) + (i*len(spaceAdd))) % 90
        shiftedSpace += alph[newIndex]
    shiftedSpace += endSpace
    return shiftedSpace

#Repeats keyword for length of message
#--------------------------------------------------------------------------------------------------------------------------------------
def keyCode(newKeyword, newText):
    newCode = ''
    for i in range(len(newText)):
        keyIndex = i % len(newKeyword)
        newCode += newKeyword[keyIndex]
    return newCode

#Encrypts Message against repeated keyword using the Vignere Cipher
#--------------------------------------------------------------------------------------------------------------------------------------
def encrypt(newText, newCode, type):
    fullCrypt = ''
    for i in range(len(newText)):
        textLetter = newText[i]
        codeLetter = newCode[i]
        textIndex = alph.index(textLetter)
        codeIndex = alph.index(codeLetter)
        if type == 'E':
            newIndex = textIndex + codeIndex
        elif type == 'D':
            newIndex = textIndex - codeIndex
        trueIndex = newIndex % 90
        cryptLetter = alph[trueIndex]
        fullCrypt += cryptLetter
    return fullCrypt

#Performs a non-caesar shift on the plain text key code so it does
#not appear in the encrypted text even if it is unscrambled
#--------------------------------------------------------------------------------------------------------------------------------------
def hideKey(keyword):
    shiftedKey = ''
    for i in range(len(keyword)):
        newIndex = (alph.index(keyword[i]) + (i*len(keyword))) % 90
        shiftedKey += alph[newIndex]
    return shiftedKey

#Scrambles the text using the Jospephus Problem
#Imagine a circle whose size is equal to the length of the scrambled text
#Run the jospehus problem n times, each time a solution is found, remove the winner from the game
#But do NOT remove it's index, this way every element of n will have a unique location in the circle
#--------------------------------------------------------------------------------------------------------------------------------------
def jospehus(combinedCodes):
    scrambledText = ''
    num = len(combinedCodes)
    codeList = []
    for i in range(len(combinedCodes)):
        codeList.append(combinedCodes[i])
    for i in range(num):
        curNum = num - i
        bit = highestBit(curNum)[0]
        pos = position(bit, curNum) 
        addChar = codeList.pop(pos-1)
        scrambledText += addChar
    return scrambledText

#END OF ENCRYPTION

#Reverses the Josephus scrambled used the encryption
#--------------------------------------------------------------------------------------------------------------------------------------
def unJo(unscrambleCode, trueList):
    truePos = []
    num = len(unscrambleCode)
    codeList = []
    for i in range(len(unscrambleCode)):
        codeList.append(unscrambleCode[i])
    for i in range(num):
        curNum = num - i
        bit = highestBit(curNum)[0]
        pos = position(bit, curNum)
        actualPos = countBodies(trueList, pos)
        trueList[actualPos] = 0
        truePos.append(actualPos + 1)
    finalCode = ''
    for i in range(len(truePos)):
        q = i + 1
        for j in range(len(truePos)):
            if truePos[j] == q:
                finalCode += codeList[j]
    return finalCode

#Counts the true index of a solution according to it's original position in the circle
#--------------------------------------------------------------------------------------------------------------------------------------
def countBodies(trueList, pos):
    numBodies = 0
    trueFound = 0
    x = 0
    while trueFound < pos:
        checkBody = trueList[x]
        if checkBody == 0:
            numBodies += 1
        elif checkBody != 0:
            trueFound += 1
        x += 1
    return x - 1

#Builds a "circle" that can be systematically unravelled
#--------------------------------------------------------------------------------------------------------------------------------------
def allBodies(scrambledText):
    trueList = []
    for i in range(len(scrambledText)):
        trueList.append(i+1)
    return trueList

#Finds the highest possible power of two given num
#--------------------------------------------------------------------------------------------------------------------------------------
def highestBit(num):
    n = 0
    found = True
    while found:
        curBit = 2**n
        if curBit > num:
            break
        else:
            n += 1
    return (curBit//2), n

#Finds the solution to each josephus problem simulation
#--------------------------------------------------------------------------------------------------------------------------------------
def position(bit, num):
    remainder = num % bit
    pos = 1 + (remainder*2)
    return pos    

#I think this one splits the keyword from the message text
#--------------------------------------------------------------------------------------------------------------------------------------
def decipher(fullMSG):
    checkDigit = fullMSG[0]
    checkIndex = alph.index(checkDigit)
    if checkIndex < 5:
        checkIndex = 5
    realCode = ''
    for i in range(checkIndex):
        y = i + 1
        realCode += fullMSG[y]
    realMSG = ''
    for i in range(len(fullMSG) - (checkIndex + 1)):
        z = i + checkIndex + 1
        realMSG += fullMSG[z]
    return realCode, realMSG

#Deciphers the Space String and returns the message without the spaces, as well as a 
#list of numbers representing indicies where spaces occur
#--------------------------------------------------------------------------------------------------------------------------------------
def decryptSpaces(finalCode):
    reverseList = ''
    removedSpaces = ''
    deSpacesAt = []
    for i in range(len(finalCode)):
        reverseList += finalCode[(len(finalCode)-(i+1))]
    
    if reverseList[0] == 'Z' and reverseList[1] == 'Z' and reverseList[2] == 'Z':
        for i in range(len(finalCode) - 3):
            removedSpaces += finalCode[i]
        return deSpacesAt, removedSpaces
    else:
        starterMult = alph.index(reverseList[0])
        starterMod = alph.index(reverseList[1])
        starterLen = (starterMult * 90) + starterMod
        removedLen = len(finalCode) - ((starterLen*2) + 2)
        for i in range(removedLen):
            removedSpaces += finalCode[i]
        spaceStr = ''
        for i in range(starterLen*2):
            spaceStr += reverseList[i+2]
        revisedStr = ''

        for i in range(len(spaceStr)):
            flip = False
            newIndex = (alph.index(spaceStr[-(i+1)]) - (i*(len(spaceStr)+2)))
            if newIndex < 0:
                newIndex *= -1
                flip = True
            newIndex = newIndex % 90
            if flip == True:
                if newIndex != 0:
                    newIndex = 90 - newIndex       
            revisedStr += alph[newIndex]
        reverseAgain = ''
        for i in range(len(revisedStr)):
            reverseAgain += revisedStr[-(i+1)]
        for i in range(starterLen):
            strMult = reverseAgain[i * 2]
            strMod = reverseAgain[(i * 2)+1]
            numMult = alph.index(strMult)
            numMod = alph.index(strMod)
            spaceNum = (numMult * 90) + numMod
            deSpacesAt.append(spaceNum)
        newSpacesAt = deSpacesAt
        return newSpacesAt, removedSpaces

#Reveals the keyword by reversing the non caesar shift used to hide the key
#The value of each shift can be determined from the len of the keyword
#--------------------------------------------------------------------------------------------------------------------------------------
def unHideKey(realCode):
    unShiftedKey = ''
    for i in range(len(realCode)):
        flip = False
        newIndex = (alph.index(realCode[i]) - (i*(len(realCode))))
        if newIndex < 0:
            newIndex *= -1
            flip = True
        newIndex = newIndex % 90
        if flip == True:
            if newIndex != 0:
                newIndex = 90 - newIndex       
        unShiftedKey += alph[newIndex]  
    return unShiftedKey

#Places the spaces back into the fully decrypted message
#--------------------------------------------------------------------------------------------------------------------------------------
def replaceSpaces(crypt, spacesAt):
    spaceText = ''
    for i in range(len(crypt)):
        if i in spacesAt:
            spaceText += ' '
        spaceText += crypt[i]
    return spaceText

#Applies an additional layer of the Vignere Cipher on top of the full scrambled string
def vignere(scrambledText, type):
    userKey = getKeyword("USER")
    print("CHECK CHECK!")
    newCodeVig = keyCode(userKey, scrambledText)
    enVig = encrypt(scrambledText, newCodeVig, type)
    return enVig

def printMSG(text):
    print('-----------------------')
    print("ENCRYPTED TEXT = ", text)
    print('-----------------------')

#ENCRYPTION
def allEn():
    try:
        plainText = getPlainText() #Check
        keyword = getKeyword("EMBEDDED") #Check
        keyLenIndex = len(keyword)
        if keyLenIndex == 5:
            keyLenIndex == len(plainText) % 6
        keyLenLetter = alph[keyLenIndex]
        newKeyword = decrpytKey(keyword) #Check
        newText, spacesAt = findSpaces(plainText) #Check
        spaceAdd = encryptSpaces(spacesAt) #Check
        shiftedSpace = shiftSpaces(spaceAdd) #Check 
        newCode = keyCode(newKeyword, newText) #Check
        encrpyted = encrypt(newText, newCode, 'E') #Check
        hiddenKeyword = hideKey(keyword) #Check
        combinedCodes = keyLenLetter + hiddenKeyword + encrpyted + shiftedSpace
        scrambledText = jospehus(combinedCodes) #Check
        return scrambledText
    except:
        print("ERROR, DOUBLE CHECK INPUT?")

#DECRYPTION
def allDe(scrambledText):
    try:
        deVig = vignere(scrambledText, 'D')
        trueList = allBodies(deVig) #Check
        finalCode = unJo(deVig, trueList) #Check
        deSpacesAt, removedSpaces = decryptSpaces(finalCode)
        realCode, splitMSG = decipher(removedSpaces)
        revealedKey = unHideKey(realCode) 
        tempCode = decrpytKey(revealedKey)
        splitCode = keyCode(tempCode, splitMSG)
        decrpyted = encrypt(splitMSG, splitCode, 'D')
        spaceTextDe = replaceSpaces(decrpyted, deSpacesAt)
        print('-----------------------')
        print("DECRYPTED TEXT = ", spaceTextDe)
        print('-----------------------')
    except:
        print("ERROR, DOUBLE CHECK INPUT?")

alph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','$','%','.','&','(',')',',','+','=',';',':','"',"'",'?','1','2','3','4','5','6','7','8','9','0','[',']','#','@','^','*','-','_','/','<','>','{','}']

menu()
print("EXITING PROGRAM")