import sys
import random
from PySide2.QtCore import *
from PySide2.QtWidgets import *



def compare(a, b):
    bull = 0
    cow = 0
    bull_s = ''
    cow_s = ''
    a_s = set(str(a))
    b_s = set(str(b))
    int_s = a_s & b_s
    for i in range(4):
        if str(a)[i] == str(b)[i]:
            bull += 1
    cow = len(int_s) - bull
    if cow == 1:
        cow_s = 'cow'
    else:
        cow_s = 'cows'
    if bull == 1:
        bull_s = 'bull'
    else:
        bull_s = 'bulls'
    return str(bull) + ' ' + bull_s + ' ' + str(cow) + ' ' + cow_s



def right_number(n):
    return len(set(str(n))) == 4 and len(str(n)) == 4 and str(n)[0] != '0'


class Game(QObject):
    flag = 0
    prev = ''
    attempts = 0
    user_message = Signal(str)

    def __init__(self):
        QObject.__init__(self)
        self.__game_num = random.randint(1000, 9999)
        while not right_number(self.__game_num):
            self.__game_num = random.randint(1000, 9999)
        print(self.__game_num)
        self.__data = ''

    def setValue(self, value):
        self.__data = value

    def guess(self, game_num):
        if self.__data.isdigit() and right_number(self.__data):
            if self.prev != self.__data:
                self.attempts += 1
            if compare(self.__data, self.__game_num) == '4 bulls 0 cows':
                self.game_win()
            else:
                self.user_message.emit(compare(self.__data, self.__game_num))
        else:
            self.user_message.emit("Incorrect number, try again!")
        self.prev = self.__data

    def game_win(self):
        self.user_message.emit('You win!\nCongratulations!' + '\nAttempts: ' + str(self.attempts))
        GuessButton.setEnabled(False)
        GiveUpButton.setText('New Game')
        self.make_leaderboard()


    def make_leaderboard(self):
        try:
            f = open('results.txt', 'r')
            a = []
            for s in f.readlines():
                num = int(s[:s.find(' ')])
                name = s[s.find(' ') + 1:]
                a.append([num, name])
            if len(a) < 5:
                self.result, self.status = QInputDialog.getText(None, "For winner", "You have won!\nWhat's your name?")
                a.append([self.attempts, self.result + '\n'])
            else:
                if a[4][0] > self.attempts:
                    self.result, self.status = QInputDialog.getText(None, "For winner", "You have won!\nWhat's your name?")
                    a[4] = [self.attempts, self.result + '\n']
            a = sorted(a)
            f.close()
            f = open('results.txt', 'w')
            for i in range(len(a)):
                f.write(' '.join(str(a[i][j]) for j in range(2)))
        except FileNotFoundError:
            f = open('results.txt', 'w')
            self.result, self.status = QInputDialog.getText(None, "For winner", "You have won!\nWhat's your name?")
            f.write(str(self.attempts) + ' ' + str(self.result) + '\n')
            f.close()



    def show_leaderboard(self):
        try:
            fin = open('results.txt', 'r')
            msgtext = ''
            с = 1
            for s in fin.readlines():
                num = s[:s.find(' ')]
                name = s[s.find(' '):-1]
                msgtext += str(с) + ' place:' + name + ' ' + num + '\n'
                с += 1
            fin.close()
        except FileNotFoundError:
            msgtext = 'No one has won yet. Do it first!'
        msgbox.setText(msgtext)
        msgbox.exec()


    def giveup(self):
        if self.__data == str(self.__game_num) or self.flag == 1:
            LineEdit.setText('')
            GiveUpButton.setText('Give up')
            self.user_message.emit('')
            self.__game_num = random.randint(1000, 9999)
            while not right_number(self.__game_num):
                self.__game_num = random.randint(1000, 9999)
            print(self.__game_num)
            self.__data = ''
            GuessButton.setEnabled(True)
            self.attempts = 0
            self.flag = 0
            self.prev = ''
        else:
            self.user_message.emit('You lose!\nRight number: ' + str(self.__game_num) + '\nTry again!')
            GiveUpButton.setText('New Game')
            LineEdit.setText('')
            GuessButton.setEnabled(False)
            self.flag = 1






app = QApplication(sys.argv)
Window = QMainWindow()
Window.resize(500, 300)
GuessButton = QPushButton('Guess', Window)
GuessButton.setGeometry(180, 160, 70, 30)

msgbox = QMessageBox()
user_text = QLabel(Window)
user_text.setGeometry(60, 220, 300, 60)
LineEdit = QLineEdit(Window)
LineEdit.setGeometry(180, 110, 140, 40)

GiveUpButton = QPushButton('Give up', Window)
GiveUpButton.setGeometry(250, 160, 70, 30)

LeaderboardButton = QPushButton('Leaderboard', Window)
LeaderboardButton.setGeometry(180, 200, 140, 40)

MyGame = Game()

GiveUpButton.clicked.connect(MyGame.giveup)
GuessButton.clicked.connect(MyGame.guess)
LeaderboardButton.clicked.connect(MyGame.show_leaderboard)
MyGame.user_message.connect(user_text.setText)
LineEdit.textChanged.connect(MyGame.setValue)


Window.show()
app.exec_()