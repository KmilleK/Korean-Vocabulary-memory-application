# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 23:26:04 2022

@author: camille
Before running the code:
    go in service 
    find MySQL80 and start it
"""



import sys 
import random 

from PyQt6.QtGui import QAction
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QWidget,
    QGridLayout, 
    QPushButton,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QMessageBox,
    QRadioButton,
    QButtonGroup,
    QScrollArea
)

from PyQt6.QtCore import Qt

import mysql.connector
from mysql.connector import (
    Error,
    errorcode,
    )

 
# Constant Variables definition

ERROR_MSG= "ERROR"
WINDOW_SIZE = 400

PW= "TO REPLACE WITH YOUR PASSWORD"

DB_Name='KoreanDB'

# All Needed database table definition

TABLES = {}
TABLES['chapter']=(
    "CREATE TABLE `chapter` ("
    " `ID_c` int(20) AUTO_INCREMENT,"
    " `Title` varchar(50) NOT NULL,"
    " `Topic` varchar(200) NOT NULL,"
    " PRIMARY KEY (`ID_c`)"
    ") ENGINE=InnoDB")

TABLES['word'] = (
    "CREATE TABLE `word` ("
    "  `ID_w` int(20) NOT NULL AUTO_INCREMENT,"
    "  `Korean` varchar(50) NOT NULL,"
    "  `English` varchar(50) NOT NULL,"
    "  `Type_w` varchar(20) NOT NULL,"
    "  `ID_c` int,"
    "  PRIMARY KEY (`ID_w`),"
    "  FOREIGN KEY (`ID_c`) REFERENCES `chapter` (`ID_c`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['grammar'] = (
    "CREATE TABLE `grammar` ("
    "  `ID_g` int(20) NOT NULL AUTO_INCREMENT,"
    "  `Name` varchar(30) NOT NULL,"
    "  `Type_g` varchar(20) NOT NULL,"
    "  `Rule` varchar(100) NOT NULL,"
    "  `Example` varchar(100) ,"
    "  `ID_c` int,"
    "  PRIMARY KEY (`ID_g`),"
    "  FOREIGN KEY (`ID_c`) REFERENCES `chapter` (`ID_c`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


# Message box for the database 

class DatabaseMessageBox(QMessageBox):
    def __init__(self, timeout=3, parent=None):
        super(DatabaseMessageBox, self).__init__(parent)
        self.setWindowTitle("Database")
        self.time_to_wait = timeout
        self.setText("Add information into my memory" )
        self.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        #self.setText("wait (closing automatically in {0} secondes.)".format(self.time_to_wait))
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

# Message box for the database 

class InBuildingMessageBox(QMessageBox):
    def __init__(self, timeout=3, parent=None):
        super(InBuildingMessageBox, self).__init__(parent)
        self.setWindowTitle("In Process")
        self.time_to_wait = timeout
        self.setText("This feature is not available yet. We are working on it" )
        self.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        #self.setText("wait (closing automatically in {0} secondes.)".format(self.time_to_wait))
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

# Message box when answer is correct 


class ValidAnswerMessageBox(QMessageBox):
    def __init__(self, timeout=3, parent=None):
        super(ValidAnswerMessageBox, self).__init__(parent)
        self.setWindowTitle("Testing")
        self.time_to_wait = timeout
        self.setText("You are right !!" )
        self.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        #self.setText("wait (closing automatically in {0} secondes.)".format(self.time_to_wait))
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()



# Message box when the answer is wrong 

class InvalidAnswerMessageBox(QMessageBox):
    def __init__(self, timeout=3, parent=None):
        super(InvalidAnswerMessageBox, self).__init__(parent)
        self.setWindowTitle("Testing")
        self.time_to_wait = timeout
        self.setText("Try again..." )
        self.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        #self.setText("wait (closing automatically in {0} secondes.)".format(self.time_to_wait))
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


  
# Window interface class with all the different window 
  
        
class Main_Window(QMainWindow): 
        
    def __init__(self): 
        super().__init__(parent=None)
        self.setWindowTitle("KoreanLearningapps")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        
        self._createCentralWidgetMenu()
        self._createMenu()
        self._createStatusBar()
        self.connection = self.connect_Database(PW,DB_Name)
       
    def connect_Database(self,Pw,DB_name): 
        # create server connection 
        try: 
            connection = mysql.connector.connect(host="localhost",user= "root",passwd=Pw)
            cursor =connection.cursor()
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
            self.EndSentence.setText("Error database Restart all please")
            return None
        
        #Database connection 
        try: 
            cursor.execute("USE {}".format(DB_name))
            print("Database found and in use")
        except Error as err: 
            print("Database not found")
            if err.errno==errorcode.ER_BAD_DB_ERROR:
                cursor.execute("CREATE DATABASE {}".format(DB_name))
                print("Database created successfully")
                connection.database = DB_name
        cursor.close()
        return connection 
    
    def _createMenu(self): 
        menu= self.menuBar().addMenu("&Menu")
        button_main_page=QAction("Main page",self)
        button_main_page.triggered.connect(self._createCentralWidgetMenu)
        menu.addAction(button_main_page)
        menu.addAction("&Exit",self.close)

    def _createStatusBar(self): 
        status =QStatusBar()
        status.showMessage("Put information about page")
        self.setStatusBar(status)
        
    
    # Menu window definition  

    def _createCentralWidgetMenu(self):     #Central window widget
        # layout choice 
        layout = QGridLayout()

        # first label 
        self.Title= QLabel("Today I want to ")
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.Title, 0,0,1,3)
        
        # button central line 
        
        self.LeftButton =QPushButton("MANAGE")
        layout.addWidget(self.LeftButton,1,0,1,1)
        
        self.CentralButton= QPushButton("EXPEND")
        layout.addWidget(self.CentralButton,1,1,1,1) 
        
        self.RightButton =QPushButton("STUDY")
        layout.addWidget(self.RightButton,1,2,1,1)
        
        # ending line 
        self.EndSentence =QLabel("my knowledge !!")
        self.EndSentence.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.EndSentence,2,0,1,3 )
        
        
        # set the layout in the central widget 
        window= QWidget()
        window.setLayout(layout)     
        
        self.setCentralWidget(window)
        self._connectButton()
        
    
    # Button action definition 
    
    def _connectButton(self): 
        self.CentralButton.clicked.connect(self.CB_click)
        self.RightButton.clicked.connect(self.RB_click)
        self.LeftButton.clicked.connect(self.LB_click)
      
        
    def LB_click(self):     # Left button 
        
        if self.LeftButton.text()=="MANAGE":
            self._createCentralWidgetManageDB()
            
        if self.LeftButton.text()=="Chapter":
            self._createCentralWidgedNewEntry("Chapter")
            
    def CB_click(self):         # Central button 
        
        if self.CentralButton.text()=="EXPEND":
            self.Title.setText("Expand my: ")
            self.LeftButton.setText("Chapter")
            self.CentralButton.setText("Grammar")
            self.RightButton.setText("Vocab")
            self.EndSentence.setText("today !!")
         
        elif self.CentralButton.text()=="Go to Menu":
            self._returnMainPage()
            
        elif self.CentralButton.text()=="Grammar":
            self._createCentralWidgedNewEntry("Grammar")
        
    def RB_click(self):         # Right button 
    
        if self.RightButton.text()=="STUDY":
            self._createCentralWidgetTraining() 
        
        if self.RightButton.text()=="Vocab":  
            self._createCentralWidgedNewEntry("Vocab")
            
    
    # Training window menu to select what to study
    
    def _createCentralWidgetTraining(self): 
        # layout choice 
        layout = QGridLayout()
        #layout.setVerticalSpacing(20)
        #layout.setHorizontalSpacing(20)

        # first label 
        self.Title= QLabel("I want to test myself on: ")
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.Title, 0,0,1,3)
        
        # Label on the left for choice: 
            
        self.LabelChapter = QLabel("Chapter:")
        #self.LabelChapter.setAlignment()
        #self.LabelChapter.setStyleSheet("QLabel {background-color: red;}")
        layout.addWidget(self.LabelChapter,1,0,2,1)
        
        self.BoxChapter = QComboBox()
        self.BoxChapter.addItem("All"); 
        self.FillComboBox(self.BoxChapter,"chapter","Title")
        self.BoxChapter.setCurrentIndex (-1 )
        self.BoxChapter.setFixedHeight(25)
        #self.BoxChapter.setStyleSheet("QComboBox {background-color: blue;}")
        layout.addWidget(self.BoxChapter,1,1,1,2)
       
        self.ButtonAdd =QPushButton("Add")
        self.ButtonAdd.setFixedHeight(25)
        self.ButtonAdd.clicked.connect(self.Add_chapter_study)
        layout.addWidget(self.ButtonAdd,1,3,1,1)
        
        self.LabelChapterValid=QLabel("empty")
        self.LabelChapter.setFixedHeight(25)
        layout.addWidget(self.LabelChapterValid,2,1,1,2)

        # Radio Group button         
        
        self.LabelType = QLabel("Practice Type: ")
        layout.addWidget(self.LabelType,3,0,2,1)
        
        self.RadioTypeV = QRadioButton("Vocabulary",self)
        self.RadioTypeG= QRadioButton("Grammar", self)
        
        self.RadioTypeV.toggled.connect(lambda:self.btnstate(self.RadioTypeV))
        
        self.RadioGroup = QButtonGroup(self)
        self.RadioGroup.addButton(self.RadioTypeV)
        self.RadioGroup.addButton(self.RadioTypeG)
        layout.addWidget(self.RadioTypeV, 3,1,1,1)
        layout.addWidget(self.RadioTypeG,4,1,1,1)
        
        self.RadioDirectionKE =QRadioButton("Korean -> English")
        self.RadioDirectionEK =QRadioButton("English -> Korean")
       
        self.RadioGroup2 =QButtonGroup(self)
        self.RadioGroup2.addButton(self.RadioDirectionKE)
        self.RadioGroup2.addButton(self.RadioDirectionEK)
        layout.addWidget(self.RadioDirectionKE,3,2,1,1)
        layout.addWidget(self.RadioDirectionEK,4,2,1,1)
        
        self.RadioDirectionKE.hide()
        self.RadioDirectionEK.hide()
        # button central line 
        
        self.Reset=QPushButton("Reset")
        self.Reset.clicked.connect(self.Reset_click)
        layout.addWidget(self.Reset,5,0,1,1)
        
        self.StartButton= QPushButton("Start session")
        self.StartButton.clicked.connect(self._TrainingSessionStart)
        layout.addWidget(self.StartButton,5,1,1,2) 
        
        # set the layout in the central widget 
        window= QWidget()
        window.setLayout(layout)     
        
        self.setCentralWidget(window)
    
    def btnstate(self,b):
	
      if b.text() == "Vocabulary":
         if b.isChecked() == True:
            self.RadioDirectionKE.show()
            self.RadioDirectionEK.show()
         else:
            self.RadioDirectionKE.hide()
            self.RadioDirectionEK.hide()
            self.RadioDirectionKE.setChecked(False)
            self.RadioDirectionEK.setChecked(False)
    
    def Add_chapter_study(self): 
        ChapterChoice = self.LabelChapterValid.text()
        newChapter = self.BoxChapter.currentText()
        if ChapterChoice=="All": 
            return;            
        elif ChapterChoice=="empty": 
            if newChapter=="": 
                return;
            elif newChapter=="All": 
                self.LabelChapterValid.setText(newChapter)
            else: 
                #self.LabelChapterValid.setText(" '"+newChapter+"' ")
                self.LabelChapterValid.setText(newChapter)
            #reset button call            
        else: 
            if newChapter=="All": 
                self.LabelChapterValid.setText(newChapter)
            elif newChapter in ChapterChoice: 
                self.BoxChapter.setCurrentIndex(-1)
            else: 
                #self.LabelChapterValid.setText(ChapterChoice+", '"+newChapter+"' ")
                self.LabelChapterValid.setText(ChapterChoice+","+newChapter+" ")

    def _TrainingSessionStart(self):
        
        #Get the data vector of in
        self.word_Id_testing=[]
        
        if self.RadioTypeG.isChecked(): 
            #TypeName="grammar"
            #pop up for in building 
            messagebox = InBuildingMessageBox(0, self)
            messagebox.exec()
            return
            
        
        if self.RadioTypeV.isChecked(): 
            cursor=self.connection.cursor()
            #Read the wanted tested word in database
            if self.LabelChapterValid.text()=="empty":
                self._createCentralWidgetMenu()  
            elif self.LabelChapterValid.text()=="All": 
                cursor.execute("""SELECT `ID_w` FROM word ; """)
            else:  
                # ID_c and 
                print(self.LabelChapterValid.text())
                cursor.execute("""SELECT `ID_w` FROM word WHERE `ID_c` = ( SELECT `ID_c` FROM chapter WHERE `Title` = %s); """,(self.LabelChapterValid.text(),))
            
            records = cursor.fetchall() 
            
            for row in records:
                self.word_Id_testing.append(row[0])
            
            cursor.close()
            random.shuffle(self.word_Id_testing)
            print(self.word_Id_testing)
            
         
        #Start the training     
        #preprocess
        self.total_word=len(self.word_Id_testing)
        self.Direction=True     #true if korean to english false if english to korean 
        if self.RadioDirectionEK.isChecked():
            self.Direction=False
        if self.RadioDirectionKE.isChecked(): 
            self.Direction=True
        layout = QGridLayout()
        
        cursor=self.connection.cursor()
        cursor.execute("""SELECT `Korean`,`English` FROM word WHERE `ID_w` = (%s); """,(self.word_Id_testing[0],))
        records = cursor.fetchall() 
       
        #Set visual interface 
        
        self.Title=QLabel("Training in Progress ...")
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.Title,0,0,1,1)
        
        self.LabelQuestionNumber=QLabel("{}/{}".format(self.total_word-len(self.word_Id_testing),self.total_word))
        self.LabelQuestionNumber.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.LabelQuestionNumber,1,0,1,1)
        
        if self.Direction:    #K to E
            self.LabelQuestion=QLabel(records[0][0])
            self.LabelAnswer=QLabel(records[0][1])
        else:                 # E to K 
            self.LabelQuestion=QLabel(records[0][1])
            self.LabelAnswer=QLabel(records[0][0])
        
    
        self.LabelQuestion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.LabelQuestion,2,0,1,1)
        
        self.LabelAnswer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LabelAnswer.hide()
        layout.addWidget(self.LabelAnswer,3,0,1,1)

        self.LineAnswer =QLineEdit("")
        self.LineAnswer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LineAnswer.setFocus()
        layout.addWidget(self.LineAnswer,4,0,1,1)

        self.ButtonCheck = QPushButton("Check")
        self.ButtonCheck.setDefault(True)
        self.ButtonCheck.clicked.connect(self.Checking_answer)
        layout.addWidget(self.ButtonCheck,5,0,1,1)
        
        cursor.close()
        
        window= QWidget()
        window.setLayout(layout)     
        
        self.setCentralWidget(window)
        
    def Checking_answer(self):
       #prepocess (suppress extra space at the start and the end)
       
       if self.LabelAnswer.text().lower()==self.LineAnswer.text().strip().lower():     # correct answer 
           #pop up for good answer 
           messagebox = ValidAnswerMessageBox(0, self)
           messagebox.exec()
           #check if this is the last 
           if len(self.word_Id_testing)==1:
               #finish session show finish 
               self.LabelQuestion.setText("You finish the training")
               self.LineAnswer.hide()
               
           else:
               #we update the word 
               self.word_Id_testing.pop(0)
               self.NextQuestionVocab()
           
       else:                                                   # wrong answer 
           #pop up wrong answer
           messagebox = InvalidAnswerMessageBox(0, self)
           messagebox.exec()
           if(self.LabelAnswer.isHidden()):
               self.word_Id_testing.append(self.word_Id_testing[0])
               self.LabelAnswer.show()
              
           self.LineAnswer.setText("")
           self.LineAnswer.setFocus()
                     
         
    def NextQuestionVocab(self):
        
        cursor=self.connection.cursor()
        cursor.execute("""SELECT `Korean`,`English` FROM word WHERE `ID_w` = (%s); """,(self.word_Id_testing[0],))
        records = cursor.fetchall() 
        
        self.LabelQuestionNumber.setText("{}/{}".format(self.total_word-len(self.word_Id_testing),self.total_word))
        
        if self.Direction:    #K to E
            self.LabelQuestion.setText(records[0][0])
            self.LabelAnswer.setText(records[0][1])
        else:                 # E to K 
            self.LabelQuestion.setText(records[0][1])
            self.LabelAnswer.setText(records[0][0])
            
        self.LabelAnswer.hide()

        self.LineAnswer.setText("")
        self.LineAnswer.setFocus()
        
        cursor.close()
        
    
    # Database management window (to redo)
    
    def _createCentralWidgetManageDB(self):   
    
        #layout choice 
        layout = QGridLayout()
        
        # Options for the query
   
        self.Title= QLabel("Select chapter:")
        self.Title.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.Title, 0,0,1,1)
        
        
        self.BoxChapter = QComboBox()
        self.BoxChapter.addItem("All"); 
        self.FillComboBox(self.BoxChapter,"chapter","Title")
        self.BoxChapter.setCurrentIndex (-1 )
        self.BoxChapter.setFixedHeight(25)
        #self.BoxChapter.setStyleSheet("QComboBox {background-color: blue;}")
        layout.addWidget(self.BoxChapter,0,1,1,2)
        
        
        self.Grammar_DB= QLabel("Select category:")
        self.Grammar_DB.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.Grammar_DB, 1,0,2,1)
        
        
        self.RadioTypeV = QRadioButton("Vocabulary",self)
        self.RadioTypeG= QRadioButton("Grammar", self)
        
        
        self.RadioGroup = QButtonGroup(self)
        self.RadioGroup.addButton(self.RadioTypeV)
        self.RadioGroup.addButton(self.RadioTypeG)
        self.RadioGroup.exclusive()
        layout.addWidget(self.RadioTypeV, 1,1,1,1)
        layout.addWidget(self.RadioTypeG,2,1,1,1)
   
        
        self.Reset=QPushButton("Reset")
        self.Reset.clicked.connect(self.Reset_click)
        layout.addWidget(self.Reset,3,0,1,1)
        
       
        # exemple of use of FillTableLayout 
        
        self.ScrollGrid=QScrollArea(self)
        self.ScrollGrid.setWidgetResizable(True)
        self.ScrollGridWidgetContents=QWidget()
      
        self.TableOfData = QGridLayout(self.ScrollGridWidgetContents)       
        self.ScrollGrid.setWidget(self.ScrollGridWidgetContents)
        layout.addWidget(self.ScrollGrid,4, 0, 1,3)
        
        self.HideAllTableLayout()
        
        
        self.Request_button=QPushButton("Request data")
        self.Request_button.clicked.connect(self.FillTableLayout)
        layout.addWidget(self.Request_button,3,2,1,1)
        
       
        # set the layout in the central widget 
        window= QWidget()
        window.setLayout(layout)     
        
        self.setCentralWidget(window)
        
        
        
            

    def FillTableLayout(self):
        # Database retrieve 
        
        for i in reversed(range(self.TableOfData.count())):
            widget = self.TableOfData.itemAt(i).widget()
            if widget is not None:
                self.TableOfData.removeWidget(widget)
                widget.deleteLater()
                
        
        cursor=self.connection.cursor()
        try:
            if self.RadioTypeG.isChecked():
                messagebox = InBuildingMessageBox(0, self)
                messagebox.exec()
                
                
            if self.RadioTypeV.isChecked():
                cursor.execute("""SELECT * FROM word WHERE `ID_c` = ( SELECT `ID_c` FROM chapter WHERE `Title` = %s); """ ,(self.BoxChapter.currentText(),))
                records = cursor.fetchall()
                
                
                for i in range(len(cursor.description)):
                    desc = cursor.description[i]
                    self.TableOfData.addWidget(QLabel("{}".format(desc[0])),0,i,1,1)
                
                i=0
                for row in records:
                    i=i+1
                    for col in range(1,len(row)-1):
                        self.TableOfData.addWidget(QLabel("{}".format(row[col])),i,col,1,1)
                        
                
        except mysql.connector.Error as err: 
            print(f"Error: '{err}'")
        cursor.close()
        self.ShowAllTableLayout()
        
    
    def ShowAllTableLayout(self):
        for i in range(self.TableOfData.count()):
            widget = self.TableOfData.itemAt(i).widget()
            widget.setVisible(True)
        
          
        
    
    def HideAllTableLayout(self):
        for i in range(self.TableOfData.count()):
            widget = self.TableOfData.itemAt(i).widget()
            widget.setVisible(False)
        
        
    # Add new entry in the database window 
    
    def _createCentralWidgedNewEntry(self,entry_type):     #Central window widget 
        
        # layout choice 
        layout = QGridLayout()
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(20)
        
        # first label 
        self.Title= QLabel("New Chapter")
        self.Title.setFixedHeight(20)
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.Title, 0,0,1,2)
        
        
        if entry_type=="Chapter":
            self.Title.setText("new Chapter")
            # label of left column
            self.LabelTitle = QLabel("Title")
            self.LabelTitle.setFixedHeight(25)
            layout.addWidget(self.LabelTitle, 1,0,1,1)
            
            self.LabelTopic =QLabel("Topic")
            self.LabelTopic.setFixedHeight(25)
            layout.addWidget(self.LabelTopic,2,0,1,1)
            
            # Typing input
            self.LineTitle =QLineEdit(self)
            self.LineTitle.setFixedHeight(25)
            layout.addWidget(self.LineTitle,1,1,1,1)
            
            
            self.LineTopic =QTextEdit(self)
            self.LineTopic.setFixedHeight(100)
            layout.addWidget(self.LineTopic,2,1,1,1)
            
            
            #Button for validation or reset 
            self.Add= QPushButton("ADD")
            self.Add.setFixedWidth(90)
            layout.addWidget(self.Add,3,0,1,1,Qt.AlignmentFlag.AlignCenter) 
            self.Add.clicked.connect(self.chapter_row_addition)
        
            self.Reset =QPushButton("RESET")
            self.Reset.setFixedWidth(90)
            layout.addWidget(self.Reset,3,1,1,1,Qt.AlignmentFlag.AlignCenter)
        
        
        if entry_type=="Grammar":
            
            self.Title.setText("new Grammar")
            
            # label of left column
            self.LabelName = QLabel("Name")
            self.LabelName.setFixedHeight(25)
            layout.addWidget(self.LabelName, 1,0,1,1)
            
            self.LabelChapter =QLabel("Chapter")
            self.LabelChapter.setFixedHeight(25)
            layout.addWidget(self.LabelChapter,2,0,1,1)
            
            self.LabelType = QLabel("Type")
            self.LabelType.setFixedHeight(25)
            layout.addWidget(self.LabelType, 3,0,1,1)
            
            self.LabelRule =QLabel("Rule")
            self.LabelRule.setFixedHeight(25)
            layout.addWidget(self.LabelRule,4,0,1,1)
           
            self.LabelExample = QLabel("Example")
            self.LabelExample.setFixedHeight(25)
            layout.addWidget(self.LabelExample, 5,0,1,1)
            
            # Typing input
            
            self.LineName =QLineEdit(self)
            self.LineName.setFixedHeight(25)
            layout.addWidget(self.LineName,1,1,1,1)
            
            #Chapter combo box 
            self.BoxChapter = QComboBox()
            self.FillComboBox(self.BoxChapter,"chapter","Title")
            self.BoxChapter.setFixedHeight(25)
            self.BoxChapter.setCurrentIndex (-1 )
            layout.addWidget(self.BoxChapter,2,1,1,1)
           
            #type combo box 
            self.BoxType = QComboBox()
            self.BoxType.setFixedHeight(25)
            self.BoxType.addItem("Conjugaison")
            self.BoxType.addItem("Irregular verbe")
            self.BoxType.addItem("particle")
            self.BoxType.setCurrentIndex (-1 )
            layout.addWidget(self.BoxType, 3,1,1,1)
            
            self.LineRule =QTextEdit(self)
            self.LineRule.setFixedHeight(60)
            layout.addWidget(self.LineRule,4,1,1,1)
            
            self.LineExamples =QTextEdit(self)
            self.LineExamples.setFixedHeight(40)
            layout.addWidget(self.LineExamples,5,1,1,1)
            
            #Button for validation or reset 
            self.Add= QPushButton("ADD")
            self.Add.setFixedWidth(90)
            self.Add.clicked.connect(self.grammar_row_addition)
            layout.addWidget(self.Add,6,0,1,1,Qt.AlignmentFlag.AlignCenter) 
            
        
            self.Reset =QPushButton("RESET")
            self.Reset.setFixedWidth(90)
            layout.addWidget(self.Reset,6,1,1,1,Qt.AlignmentFlag.AlignCenter)
            
            
        if entry_type=="Vocab":
            
            self.Title.setText("new Vocabulary")
            
            # label of left column
            
            self.LabelChapter =QLabel("Chapter")
            self.LabelChapter.setFixedHeight(25)
            layout.addWidget(self.LabelChapter,1,0,1,1)
            
            self.LabelKorean = QLabel("Korean")
            self.LabelKorean.setFixedHeight(25)
            layout.addWidget(self.LabelKorean, 2,0,1,1)
            
            self.LabelEnglish = QLabel("English")
            self.LabelEnglish.setFixedHeight(25)
            layout.addWidget(self.LabelEnglish, 3,0,1,1)
            
            self.LabelType = QLabel("Type")
            self.LabelType.setFixedHeight(25)
            layout.addWidget(self.LabelType, 4,0,1,1)            
            # Typing input
            
            #Chapter combo box 
            
            self.BoxChapter = QComboBox()
            self.FillComboBox(self.BoxChapter,"chapter","Title")
            self.BoxChapter.setFixedHeight(25)
            self.BoxChapter.setCurrentIndex (-1 )
            layout.addWidget(self.BoxChapter,1,1,1,1)
            
            self.LineKorean =QLineEdit(self)
            self.LineKorean.setFixedHeight(25)
            layout.addWidget(self.LineKorean,2,1,1,1)
            
            self.LineEnglish =QLineEdit(self)
            self.LineEnglish.setFixedHeight(25)
            layout.addWidget(self.LineEnglish,3,1,1,1)
            
            self.BoxType = QComboBox()
            self.BoxType.addItem("Noun")
            self.BoxType.addItem("Verbs")
            self.BoxType.setFixedHeight(25)
            self.BoxType.setCurrentIndex (-1 )
            layout.addWidget(self.BoxType,4,1,1,1)
            
            
            #Button for validation or reset
            
            self.Add= QPushButton("ADD")
            self.Add.setFixedWidth(90)
            self.Add.clicked.connect(self.word_row_addition)
            layout.addWidget(self.Add,5,0,1,1,Qt.AlignmentFlag.AlignCenter) 
            
        
            self.Reset =QPushButton("RESET")
            self.Reset.setFixedWidth(90)
           
            layout.addWidget(self.Reset,5,1,1,1,Qt.AlignmentFlag.AlignCenter)
        
        
        # set the layout in the central widget 
        self.Reset.clicked.connect(self.Reset_click)
        
        window= QWidget()
        window.setLayout(layout)     
        self.setCentralWidget(window)
    
    def chapter_row_addition(self):
       cursor=self.connection.cursor()
       try: 
           cursor.execute("""INSERT INTO chapter(`Title`,`Topic`) VALUES (%s, %s);""", (self.LineTitle.text(), self.LineTopic.toPlainText()))
           self.connection.commit()
           messagebox = DatabaseMessageBox(0, self)
           messagebox.exec()      
       except mysql.connector.Error as err: 
           print(f"Error: '{err}'")
       cursor.close()
       
       
    def word_row_addition(self):
       cursor=self.connection.cursor()
       try: 
           # get chapter Id associate to the box 
           cursor.execute("""SELECT `ID_c` FROM chapter WHERE `Title`= %s; """,(self.BoxChapter.currentText(),))
           records = cursor.fetchall() 
           for row in records:
               Id=row[0]
           cursor.execute("""INSERT INTO word(`Korean`,`English`,`Type_w`,`ID_c`) VALUES (%s, %s , %s, %s);""", (self.LineKorean.text(),self.LineEnglish.text(),self.BoxType.currentText(),Id))
           self.connection.commit()
           messagebox = DatabaseMessageBox(0, self)
           messagebox.exec()
       except mysql.connector.Error as err: 
           print(f"Error: '{err}'")
       cursor.close()
          
    def grammar_row_addition(self):
       cursor=self.connection.cursor()
       try: 
           # get chapter Id associate to the box 
           cursor.execute("""SELECT `ID_c` FROM chapter WHERE `Title`= %s; """,(self.BoxChapter.currentText(),))
           records = cursor.fetchall() 
           for row in records:
               Id=row[0]
           
           cursor.execute("""INSERT INTO grammar(`Name`,`Type_g`,`Rule`,`Example`,`ID_c`) VALUES(%s, %s, %s, %s, %s);""",(self.LineName.text(),self.BoxType.currentText(),self.LineRule.toPlainText(),self.LineExamples.toPlainText(),Id))
           self.connection.commit()
           messagebox = DatabaseMessageBox(0, self)
           messagebox.exec()
           
       except mysql.connector.Error as err: 
           print(f"Error: '{err}'")
       cursor.close()
            
    def FillComboBox(self,Box,Table,entry_name):
        # Database retrieve 
        cursor=self.connection.cursor()
        try:
            cursor.execute("SELECT {} FROM {}".format(entry_name,Table))
            records = cursor.fetchall()
            
            for row in records:
               Box.addItem("{}".format(row[0]))
                    #Layout.addWidget(QLabel("{}".format(row[col])),i,col,1,1)
                    
                
        except mysql.connector.Error as err: 
            print(f"Error: '{err}'")
        cursor.close()

       
    def Reset_click(self):
        if self.Title.text()=="new Chapter":
            self.LineTitle.clear()
            self.LineTopic.clear()
            
        elif self.Title.text()=="new Grammar":
            self.LineName.clear()
            self.LineRule.clear()
            self.LineExamples.clear()
            self.BoxChapter.setCurrentIndex (-1 )
            self.BoxType.setCurrentIndex (-1 )
            
        elif self.Title.text()=="new Vocabulary": 
            self.LineKorean.clear()
            self.LineEnglish.clear()
            self.BoxChapter.setCurrentIndex (-1 )
            self.BoxType.setCurrentIndex (-1 )
        
        elif self.Title.text()=="I want to test myself on: ":
            self.LabelChapterValid.setText("empty")
            self.BoxChapter.setCurrentIndex (-1 )
            self.RadioGroup.setExclusive(False)
            self.RadioTypeG.setChecked(False)
            self.RadioTypeV.setChecked(False)
            self.RadioGroup.setExclusive(True)
            self.RadioGroup2.setExclusive(False)
            self.RadioDirectionKE.setChecked(False)
            self.RadioDirectionEK.setChecked(False)
            self.RadioGroup2.setExclusive(True)
            
        elif self.Title.text()=="Select chapter:":
            self.BoxChapter.setCurrentIndex (-1 )
            self.RadioGroup.setExclusive(False)
            self.RadioTypeG.setChecked(False)
            self.RadioTypeV.setChecked(False)
            self.HideAllTableLayout()
            
            
            
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                    "Are you sure to quit?", QMessageBox.StandardButton.Yes |
                    QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.connection.close()
            event.accept()
        else:

            event.ignore()
    
       
def main(): 
    "Main function"
    app=QApplication([])
    "looking part of the apps"
    main_window = Main_Window()
    main_window.show()
    sys.exit(app.exec())
    
    
    
if __name__ == "__main__": 
    main()
    