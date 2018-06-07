from PyQt5.QtGui import QFont , QColor , QTextCharFormat , QSyntaxHighlighter
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow , QFileDialog , QApplication , qApp ,QLineEdit ,QMessageBox
from PyQt5.uic import loadUiType
from os import path
from sys import argv
import re

#>---------------------------------------------------------------------------------------------------------------------<

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.Recognizer()
        self.Auther = "//Author : Cyber_hunter\n\n"
        self.plainTextEdit.insertPlainText(self.Auther)

    def Handle_Buttons(self):
        self.actionNew_File.triggered.connect(self.New_file)
        self.actionNew_File.setShortcut("Ctrl+N")
        self.actionFile.triggered.connect(self.Open_file)
        self.actionFile.setShortcut("Ctrl+O")
        self.actionSave_2.triggered.connect(self.Save_file)
        self.actionSave_2.setShortcut("Ctrl+S")
        self.actionSave_as.triggered.connect(self.SaveAs_file)
        self.actionExit.triggered.connect(qApp.quit)
        self.actionZoom_in.triggered.connect(self.Zoom_In)
        self.actionZoom_in.setShortcut("Ctrl++")
        self.actionZoom_out.triggered.connect(self.Zoom_Out)
        self.actionZoom_out.setShortcut("Ctrl+-")
        self.actionRedo.triggered.connect(self.Redo)
        self.actionRedo.setShortcut("Ctrl+R")

    def New_file(self):
        global file_name
        file_name = "Untitled"
        self.plainTextEdit.clear()
        self.plainTextEdit.insertPlainText(self.Auther)

    def Open_file(self):
        try:
            self.file_name = QFileDialog.getOpenFileName(self ,directory='.' , filter= "*.py *.java")
            print(self.file_name)
            x = open(self.file_name[0], "rt")
            self.plainTextEdit.clear()
            self.plainTextEdit.insertPlainText(self.Auther)
            self.plainTextEdit.insertPlainText(x.read())
        except Exception as e:
            print(e)

    def Save_file(self):
        text = self.plainTextEdit.toPlainText()
        try:
            self.file_name = QFileDialog.getSaveFileName(self, directory='.' , filter="*.py *.java")
            with open(self.file_name[0], "wt") as file:
                file.write(text)
                file.close()
        except Exception as e :
            print(e)

    def SaveAs_file(self):
        text = self.plainTextEdit.toPlainText()
        try:
            self.file_name = QFileDialog.getSaveFileName(self, directory='.' ,filter="*.py *.java")
            with open(self.file_name[0], "wt") as file:
                file.write(text)
                file.close()
        except Exception as e:
            print(e)

    def Zoom_In(self):
        self.plainTextEdit.zoomIn(range=2)

    def Zoom_Out(self):
        self.plainTextEdit.zoomOut(range=2)

    def Undo(self):
        self.plainTextEdit.undo()

    def Redo(self):
        self.plainTextEdit.redo()

    def Recognizer(self):
        self.editor = self.plainTextEdit.document()
        self.highlighter = Recognition(self.editor)


#>---------------------------------------------------------------------------------------------------------------------<


def format(color , style = ''):
    set_color = QColor()
    set_color.setNamedColor(color)
    format = QTextCharFormat()
    format.setForeground(set_color)
    if "bold" in style :
        format.setFontWeight(QFont.Bold)
    if "italic" in style :
        format.setFontItalic(True)
    if "underline" in style :
        set_color.setNamedColor("red")
        format.setFontUnderline(True)
        format.setUnderlineColor(set_color)

    return format

STYLES = {
    'keyword'  : format('cyan' ,'bold') ,
    'operator' : format('red') ,
    'brace'    : format('brown') ,
    'comment'  : format('gray', 'italic , bold') ,
    'string'   : format('magenta') ,
    'numbers'  : format('yellow') ,
    'class'    : format('blue' , 'bold') ,
    'default'  : format('white') ,
    'error'    : format('white' , 'underline') ,
    'operation': format('green' , 'bold')
    }

#>---------------------------------------------------------------------------------------------------------------------<

INTEGER, PLUS, MINUS, MULT, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULT' , 'DIV', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULT, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        elif op.type == MULT:
            self.eat(MULT)
        elif op.type == DIV:
            self.eat(DIV)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        elif op.type == MULT:
            result = left.value * right.value
        elif op.type == DIV:
            result = left.value / right.value
        return result


#>---------------------------------------------------------------------------------------------------------------------<


class Recognition(QSyntaxHighlighter):
    keywords = [
        'break', 'class', 'continue', 'def' , 'main' ,
        'del', 'elif', 'else', 'except', 'finally', 'print' ,
        'for', 'from', 'global', 'if', 'import', 'show' ,
        'return' , 'try', 'while', 'self' , 'open' , 'close',
        '__init__' , '__main__' , '__name__' ,'True' ,
        'False' , 'None' , 'and' , 'or' , 'not' , 'pass' ,
        'is' , 'in'
    ]

    operators = [
        '=' , '!' , '==', '!=', '<', '<=', '>', '>=', '%' , '\+' , '-' , '/' , '\*' ,
    ]

    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self,document):
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        rules += [
                  ('[^\s.*.]', 0, STYLES['error']),
                  (r'[:]', 0, STYLES['default'])]

        rules += [
                  (r'\b%s\b\s*(\w+(\.)\w+)' % x, 1, STYLES['default'])                      #
                        for x in Recognition.keywords]

        rules += [
            (r'\b%s\b\s*(\w+\s*(\,)*\s*\w+)' % x, 1, STYLES['default'])  #
            for x in Recognition.keywords]

        rules += [
                  (r'\b%s\b\s*(\w+)' % x, 1, STYLES['default'])  #
                        for x in Recognition.keywords]

        rules += [
                  (r'\([^\)\\]*(\\.[^\(\\]*)*.', 0, STYLES['error']),
                  (r'\([^\)\\]*(\\.[^\(\\]*)*\)', 0, STYLES['default']),
                  (r'\[[^\]\\]*(\\.[^\[\\]*)*.', 0, STYLES['error']),
                  (r'\[[^\]\\]*(\\.[^\[\\]*)*\]', 0, STYLES['default']),
                  (r'\{[^\}\\]*(\\.[^\{\\]*)*.', 0, STYLES['error']),
                  (r'\{[^\}\\]*(\\.[^\{\\]*)*\}', 0, STYLES['default'])]

        rules += [(r'(.*.)=', 0, STYLES['default'])]

        rules += [
                 (r'\b%s\b' % w, 0, STYLES['keyword'])
                        for w in Recognition.keywords]

        rules += [
                  (r'%s' % o, 0, STYLES['operator'])
                        for o in Recognition.operators]

        rules += [
                  (r'\b[0-9]+[eE]?\b', 0, STYLES['numbers']) ,
                  (r'"[^"\\]*(\\.[^"\\]*)*.', 0, STYLES['error']) ,
                  (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']) ,
                  (r"'[^'\\]*(\\.[^'\\]*)*.", 0, STYLES['error']) ,
                  (r'\'[^\'\\]*(\\.[^\'\\]*)*\'', 0, STYLES['string'])]

        rules += [
                  (r'\bclass\b\s*(\w+)', 1, STYLES['error']) ,
                  #(r'\bclass\b\s*(\w+\s*(\(\))\s*(\:))', 1, STYLES['class']) ,
                  (r'\bclass\b\s*([0-9]*\w*)', 1, STYLES['error']),
                  (r'\b\bclass\b\s*(\w+)\b\s*(\((\w*)\))\s*(\:)', 1, STYLES['class']),
                  (r'\b\bclass\b\s*(\w+)\b\s*(\((\w*)\))\s*(\:)', 4, STYLES['class']),
                  (r'\bdef\b\s*(\w+)', 1, STYLES['error']),
                  (r'\bdef\b\s*(\w+\s*(\(\))\s*(\:))', 1, STYLES['class']),
                  (r'\bdef\b\s*([0-9]\w+)', 1, STYLES['error']),
                  (r'\b\bdef\b\s*(\w+)\b\s*(\((\w+)\))\s*(\:)', 1, STYLES['class']),
                  (r'\b\bdef\b\s*(\w+)\b\s*(\((\w+)\))\s*(\:)', 4, STYLES['class']),]

        rules += [
                 (r'%s' % b, 0, STYLES['brace'])
                        for b in Recognition.braces]

        rules += [(r'#[^\n]*', 0, STYLES['comment'])]

        rules += [(r'\bfor\b\s*(\w+)\s(\w+)\s(\w+)(\([0-9]+\))\:',0,STYLES['operation']),
                  (r'[0-9]+\s*\+\s*[0-9]+;', 0, STYLES['operation']),
                  (r'[0-9]+\s*\-\s*[0-9]+;', 0, STYLES['operation']),
                  (r'[0-9]+\s*\*\s*[0-9]+;', 0, STYLES['operation']),
                  (r'[0-9]+\s*\/\s*[0-9]+;', 0, STYLES['operation'])]

        self.rules = [
                      (QRegExp(pat), index, fmt)
                            for (pat, index, fmt) in rules
                     ]

    def highlightBlock(self, text):
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        operations = ['\+', '\-','\*','\/']
        op_rules = []
        op_rules += [re.findall('[0-9]+\s*{}\s*[0-9]+;'.format(x), text)
                     for x in operations]
        for rule in op_rules:
            if rule != []:
                parser = Interpreter(rule[0].replace(';',''))
                result = parser.expr()
                print(result)

        self.setCurrentBlockState(0)

#>---------------------------------------------------------------------------------------------------------------------<

def main() :
    app = QApplication(argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
