#--disable=unused-wildcard-import,invalid-name,missing-docstring,wildcard-import
Letters_path = R"C:\Users\Egor\Documents\temp\letters"

import json
import codecs
import sys
import IRNodes

class TokenEx(IRNodes.Token):
    def initSetting(self):
        if ' ' == self.token:
            self.file = ""
        else:
            self.file = "{0}\{1}\{1}.png".format(Letters_path, self.token)

    def __init__(self, token):
        super().__init__(token)
        self.initSetting()
        

class WordEx(IRNodes.Word):
    def createTokens(self, strWord):
        return [TokenEx(x) for x in strWord]

    def __init__(self, strWord):
        super().__init__(strWord)


class LineEx(IRNodes.Line):
    def createWords(self, lWords):
        return [WordEx(word) for word in lWords]

    def __init__(self, strLine):
        super().__init__(strLine)


def createIR(file):
    if (not file):
        print("No file specified")

    else:
        lLines = []
        
        with codecs.open(file, 'r', "utf8") as fin:
            for line in fin:
                lLines.append(LineEx(line[:-2]).getAttrsRec())

        return lLines 

if "__main__" == __name__:
    file = sys.argv[1]

    if (not file):
        print("No file specified")

    else:
        lLines = []
        
        with codecs.open(file, 'r', "utf8") as fin:
            for line in fin:
                lLines.append(LineEx(line[:-2]).getAttrsRec())

        with codecs.open("{0}.json".format(file.split('.')[0]), 'w', "utf8") as fout:
            json.dump(lLines, fout, indent = 4, ensure_ascii=False)