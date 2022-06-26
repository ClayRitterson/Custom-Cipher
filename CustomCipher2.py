# Custom Cipher
# Written by: CWR, 2022

#SAMPLE ENCRYPTIONS
#--------------------------------------------------------------------------------------------------------------------------------------
# ARJXLBUKZODWNDTIBPGZPIFXNEVKATIXQEUWLCOPWALJMWVNEGRACBDIXWCCPIAHCNHPWWTLPYXWTAAVKAQWACNPCCWSMPGLNPVHVQPGRANBXVQQVBDFXAIZWIIBCOMKJHFECAZXWUTRPOQHZGTLWAXPDFRRAZHMRGJCHQUDQRKWYDWYSVDDKPDDUHBJAWTQMJGDANKMJWLFFHGUCPZDYSUMWGRKVOIBNJRDWFGJLSQYLWKYVKRSCSWFSZ
#--------------------------------------------------------------------------------------------------------------------------------------
# TOMCKFBWHBRXYGNYYIVNPSZWGXCLGHGFRZAPNBUEUCPPGRKXMWKEVZJRAXMYDDYGVWAUZJDTUTYIQSMBAKEFQQNIXQDAUOICWRLFZTNHCWQKEYSNHBVPJEYSMGAVPJDXRLFAUOICWQLFZTNHCWQKEYSNHBVPJDYSMGAUOIDXRLFZTOICWQLFZTNHBWQKEPIMVRCRWCMRFCUPHFQRYRVJREUIMTOUQVZTGRPUPNFTYUUVJLTYYNLZCHZRYYSJDNFEEMCTYSPZKJHHRABZRPDLYVEGHHFQRYWLJBUEUMHCCRKYGHHLBVLEMAAHUBEEJLOVNYPCASHMYONLXUCUCJMFNIVLBCUHFEYSPMIGZUTLOIFYVNGBXTOMGEZRPNIEBVQJEYUOLJIEYTQMEFCEVVZRLGUKBDAMMEGTURMBLEMIUYBCVXIYMDYIGTQFMIVXBBNMETMOIIMACOJQTBESPJYIGNCCSGMGULJYOKCSEWLDUPIXNBRLDWNHPGSXUPQFNMAAJNVIBABFCTLRBFERTAZGBKPPKSFQDPXYHTCENZIGVIVCBNVQCUGUEUCTOWCRKCTGVIRJYWGYICMSYCQFBSGUXBMRH
#--------------------------------------------------------------------------------------------------------------------------------------
# ATVMLDLKASRKHKFQLGLDZLBBQJAKOSWAEINRVZDHLPUYCGKPTXBXULNZXZUZPTTTOEAZQNWULTVQQLODAXFCZYDHXOYZNBPDSHXOJWJCFAOEATKWLKFAJBZAZLRVVBHOKQFOQGWZYUFLWDXFSDIDUCOKZ
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
        elif select == '2':
            userScram = inputScrambled()
            allDe(userScram)
        elif select == '3':
            scrambledText = allEn()            
            allDe(scrambledText)
        elif select == '4':
            break

def getKeyword():
    valid = False
    while valid == False:
        keyword = str(input("Enter Keyword: "))
        if keyword.isalpha() == False:
            print("Keyword can only contain letters A-Z")
        elif len(keyword) < 5 or len(keyword) > 25:
            print("Keyword must be between 5 and 25 letters long")
        else:
            valid = True
    return keyword.upper()

def getPlainText():
    valid = False
    while valid == False:
        newText = ''
        plainText = str(input("Enter the message to encrypt: "))
        for i in range(len(plainText)):
            if plainText[i] != ' ':
                newText += plainText[i]
        if newText.isalpha() == False:
            print("Message must only contains letters A->Z and spaces")
        elif len(newText) > 600:
            print("Message must be 600 characters or less, including spaces")
            print("Message is currently ", len(newText), " characters long")
        else:
            valid = True
    return plainText.upper()

def inputScrambled():
    validScram = False
    while validScram == False:
        inputScram = str(input("ENTER ENCRYPTED TEXT: "))
        if len(inputScram) > 0 and inputScram.isalpha():
            validScram = True
        else:
            print("INVALID INPUT")
    return inputScram.upper()

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
        newValIndex = (listValIndex + (shiftKey * -1)) % 26
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
            newText += plainText[i].upper()
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
        spacer = (spaceVal // 26)
        spaceMod = spaceVal % 26
        spacerLetter = alph[spacer]
        spaceModLetter = alph[spaceMod]
        crpytSpaces += spacerLetter
        crpytSpaces += spaceModLetter
    for i in range(len(crpytSpaces)):
        newSpaces += crpytSpaces[len(crpytSpaces)-(i + 1)]
    cryptSpacer = (len(spacesAt) // 26)
    cryptMod = (len(spacesAt) % 26 )
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
        newIndex = (alph.index(spaceAdd[i]) + (i*len(spaceAdd))) % 26
        shiftedSpace += alph[newIndex]
    shiftedSpace += endSpace
    return shiftedSpace

#Repeats keyword for length of message
#--------------------------------------------------------------------------------------------------------------------------------------
def keyCode(newKeyword, newText):
    newCode = ''
    for i in range(len(newText)):
        keyIndex = i % len(newKeyword)
        newCode += newKeyword[keyIndex].upper()
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
        trueIndex = newIndex % 26
        cryptLetter = alph[trueIndex]
        fullCrypt += cryptLetter
    return fullCrypt

#Performs a non-caesar shift on the plain text key code so it does
#not appear in the encrypted text even if it is unscrambled
#--------------------------------------------------------------------------------------------------------------------------------------
def hideKey(keyword):
    shiftedKey = ''
    for i in range(len(keyword)):
        newIndex = (alph.index(keyword[i]) + (i*len(keyword))) % 26
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
        starterLen = (starterMult * 26) + starterMod
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
            newIndex = newIndex % 26
            if flip == True:
                if newIndex != 0:
                    newIndex = 26 - newIndex       
            revisedStr += alph[newIndex]
        reverseAgain = ''
        for i in range(len(revisedStr)):
            reverseAgain += revisedStr[-(i+1)]
        for i in range(starterLen):
            strMult = reverseAgain[i * 2]
            strMod = reverseAgain[(i * 2)+1]
            numMult = alph.index(strMult)
            numMod = alph.index(strMod)
            spaceNum = (numMult * 26) + numMod
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
        newIndex = newIndex % 26
        if flip == True:
            if newIndex != 0:
                newIndex = 26 - newIndex       
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

#ENCRYPTION
def allEn():
    plainText = getPlainText() #Check
    keyword = getKeyword() #Check
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
    print('-----------------------')
    print("ENCRYPTED TEXT = ", scrambledText)
    print('-----------------------')
    return scrambledText

#DECRYPTION
def allDe(scrambledText):
    trueList = allBodies(scrambledText) #Check
    finalCode = unJo(scrambledText, trueList) #Check
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

alph = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

menu()
print("EXITING PROGRAM")