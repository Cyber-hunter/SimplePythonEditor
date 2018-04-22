from PyQt5.QtGui import QFont , QColor , QTextCharFormat , QSyntaxHighlighter
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow , QFileDialog , QApplication , qApp ,QLineEdit ,QMessageBox
from PyQt5.uic import loadUiType
from os import path
from sys import argv

#>----------------------------------------------------------------------------------------------------------------<

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.Recognizer()
        self.file_name = None

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
        self.actionUndo.triggered.connect(self.Undo)
        self.actionUndo.setShortcut("Ctrl+Shift+U")
        self.actionRedo.triggered.connect(self.Redo)
        self.actionRedo.setShortcut("Ctrl+Shift+R")

    def New_file(self):
        global file_name
        file_name = "Untitled"
        self.plainTextEdit.clear()

    def Open_file(self):
        self.file_name = QFileDialog.getOpenFileName(self ,directory='.' , filter= "*.txt *.py")
        self.plainTextEdit.clear()
        if self.file_name:
            with open(self.file_name[0], "rt") as file:
                self.plainTextEdit.insertPlainText(file.read())

    def Save_file(self):
        text = self.plainTextEdit.toPlainText()
        self.file_name = QFileDialog.getSaveFileName(self, directory='.' , filter="*.py")
        with open(self.file_name[0], "wt") as file:
            file.write(text)
            file.close()

    def SaveAs_file(self):
        text = self.plainTextEdit.toPlainText()
        self.file_name = QFileDialog.getSaveFileName(self, directory='.' ,filter="*.py")
        with open(self.file_name[0], "wt") as file:
            file.write(text)
            file.close()

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
    _color = QColor()
    _color.setNamedColor(color)
    _format = QTextCharFormat()
    _format.setForeground(_color)
    if "bold" in style :
        _format.setFontWeight(QFont.Bold)
    elif "italic" in style :
        _format.setFontItalic(True)
    elif "underline" in style :
        _format.setFontUnderline(True)

    return _format

STYLES = {
    'keyword': format('cyan' ,'bold'),
    'operator': format('red'),
    'brace': format('brown' , 'bold'),
    'comment': format('gray', 'italic'),
    'string': format('magenta'),
    'numbers': format('yellow'),
    'class'    : format('blue' , 'bold') ,
    'error'    : format('white' , 'underline') ,
}

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

        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in Recognition.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in Recognition.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in Recognition.braces]
        rules += [(r'//[^\n]*', 0, STYLES['comment']) ,
                  (r'"[^"\\]*(\\.[^"\\]*)*.', 0, STYLES['error']),
                  (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
                  (r"'[^'\\]*(\\.[^'\\]*)*.", 0, STYLES['error']),
                  (r'\'[^\'\\]*(\\.[^\'\\]*)*\'', 0, STYLES['string']),
                  (r'\b?[0-9]+[lL]?\b', 0, STYLES['numbers']),
                  (r'\bclass\b\s*(\w+)', 1, STYLES['class'])]

        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

#>---------------------------------------------------------------------------------------------------------------------<

def main() :
    app = QApplication(argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
