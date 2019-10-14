from PIL import Image
import json
import sys

def createA4():
    sztA4 = (2480, 3508)
    return Image.new("RGB", sztA4, (0xFF, 0xFF, 0xFF, 0xFF))

def loadIR(path):
    ir = []
    with open(path, 'r', encoding = "utf8") as fin:
        ir = json.load(fin, encoding = "utf8")
    return ir

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Writer:
    def __init__(self, ir):  
        self.img = createA4()

        self.pos = Pos(0, 0)

        self.ir = ir

        #indexes
        self.indLine = 0
        self.indWord = 0
        self.indToken = 0

    def writeText(self):
        avgLetterSize = 70
        for i in range(len(self.ir)):
            self.indLine = i

            self.writeLine()

            self.pos.x = 0
            self.pos.y += avgLetterSize +  self.ir[self.indLine]["pmTop"] + self.ir[self.indLine]["pmBot"]

        return self.img

    def writeLine(self):
        currLine = self.ir[self.indLine]

        self.pos.x += currLine["pmLeft"]
        self.pos.y += currLine["pmTop"]

        words = currLine["words"]

        for i in range(len(words)):
            self.indWord = i
            self.writeWord()

        self.pos.y -= currLine["pmTop"]
        
    
    def writeWord(self):
        currWord = self.ir[self.indLine]["words"][self.indWord]
        self.pos.x += currWord["pmLeft"]
        self.pos.y += currWord["pmTop"]

        tokens = currWord["tokens"]

        for i in range(len(tokens)):
            self.indToken = i
            self.writeToken()

        self.pos.x += currWord["pmRight"]
        self.pos.y -= currWord["pmTop"]

    def writeToken(self):
        currToken = self.ir[self.indLine]["words"][self.indWord]["tokens"][self.indToken]
        self.pos.x += currToken["pmLeft"]
        self.pos.y += currToken["pmTop"]

        if ' ' == currToken["token"]:
            self.pos.x += 30
        else:
            imToken = Image.open(currToken["file"])

            self.img.paste(imToken, (self.pos.x, self.pos.y), imToken)#

            self.pos.x += imToken.size[0] + currToken["pmRight"]

        self.pos.y -= currToken["pmTop"]

if "__main__" == __name__:
    file = sys.argv[1]
    if (not file):
        print("No IR files given")
        exit()
    else:
        ir = loadIR(file)
        writer = Writer(ir)
        img = writer.writeText()
        img.save("{0}.png".format(file.split('.')[0]))