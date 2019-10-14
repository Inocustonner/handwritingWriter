import json
import codecs
import sys
from IRNodes import Item

Letters_path = R"C:\Users\Egor\Documents\temp\letters"

class Token(Item):
    def __init__(self, token):
        super().__init__()

        self.token = token
        if (' ' != token):
            self.file = "{0}\{1}\{1}.png".format(Letters_path, self.token)

class Word(Item):
    def __init__(self):
        super().__init__()

        self.tokens = []

class Line(Item):

    @staticmethod
    def listWords(line, overlapSpaces = False):
        if (overlapSpaces):
            line = ' '.join(line.split())

        words = line.split(' ')

        for i in range(0, len(words) - 1):
            words.insert(i * 2 + 1, ' ')

        return [x for x in words if x != '']

    def __init__(self):
        super().__init__()

        self.words = []


class Parser:
    def __init__(self, file):
        if (not file):
            print("No file specified")

        self.indLine = 0
    
    def peek(self):
        if len(self.strLine) > self.indLine:
            return self.strLine[self.indLine + 1]
        else:
            return ''

    def glimps(self):
        if 0 < len(self.strLine):
            return self.strLine[self.indLine - 1]
        else:
            return ''

    def token(self, cToken):
        token = Token(cToken)
        return token

    def word(self, strWord):
        word = Word()
        for token in list(strWord):
            word.tokens.append(self.token(token))
            self.indLine += 1
        return word

    def line(self, strLine):
        self.strLine = strLine
        self.indLine = 0

        line = Line()
        for word in Line.listWords(strLine):
            line.words.append(self.word(word))
        return line


    def parse(self):
        lLines = []
        
        with codecs.open(file, 'r', "utf8") as fin:
            for line in fin:
                #lLines.append(LineEx(line[:-2]).getAttrsRec())
                lLines.append(self.line(line[:-2]).getAttrsRec())

        return lLines 

if "__main__" == __name__:
    file = sys.argv[1]

    if (not file):
        print("No file specified")

    else:
        p = Parser(file)
        with codecs.open("{0}.json".format(file.split('.')[0]), 'w', "utf8") as fout:
            json.dump(p.parse(), fout, indent = 4, ensure_ascii=False)