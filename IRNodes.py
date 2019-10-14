class Token:
    def __init__(self, token):
        assert type(token) == str

        self.token = token

        self.file = ""

        self.pmTop = 0
        self.pmBot = 0
        self.pmRight = 0
        self.pmLeft = 0

        self.rotAngle = 0

    def getAttrs(self):
        return vars(self)

class Word:    
    def createTokens(self, strWord):
        return list(map(lambda x: Token(x), list(strWord)))

    def __init__(self, strWord):
        assert type(strWord) == str

        self.tokens = self.createTokens(strWord)

        self.pmTop = 0
        self.pmBot = 0
        self.pmRight = 0
        self.pmLeft = 0

        self.rotAngle = 0

    def getAttrs(self):
        return vars(self)

    def getAttrsRec(self):
        attrs = dict()
        for x in vars(self):

            if "tokens" == x:
                attrs[x] = list()

                for token in getattr(self, x):
                    attrs[x].append(token.getAttrs())

            else:
                attrs[x] = getattr(self, x)

        return attrs


class Line:
    @staticmethod
    def listWords(line, overlapSpaces = False):
        if (overlapSpaces):
            line = ' '.join(line.split())

        words = line.split(' ')

        for i in range(0, len(words) - 1):
            words.insert(i * 2 + 1, ' ')

        return [x for x in words if x != '']

    def createWords(self, lWords):
        return list(map(lambda x: Word(x), lWords))

    def __init__(self, strLine):
        assert type(strLine) == str

        lWords = Line.listWords(strLine)

        self.words = self.createWords(lWords)

        self.pmTop = 0
        self.pmBot = 0
        self.pmRight = 0
        self.pmLeft = 0

        self.rotAngle = 0

    def getAttrs(self):
        return vars(self)

    def getAttrsRec(self):
        attrs = dict()
        for x in vars(self):

            if "words" == x:
                attrs[x] = list()

                for word in getattr(self, x):
                    attrs[x].append(word.getAttrsRec())

            else:
                attrs[x] = getattr(self, x)

        return attrs