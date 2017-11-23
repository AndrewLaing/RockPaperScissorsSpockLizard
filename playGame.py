###############################################################################
## Filename     : playGame.py
## Author       : Andrew Laing (parisianconnections@gmail.com)
## Source       : Python 3.5
## Description  : A Tkinter GUI for the game;
## History      : Work started 29/09/2015
###############################################################################

import tkinter, rpssl
from os import path
from utils import saveToPickle
import img.images as images


class RPSSLGui:
    def __init__(self, rpssl):
        self.rpssl = rpssl
        self.setMainVariables()
        self.loadImages()
        self.createWidgets()
        self.showWelcomeScreen()


    def setMainVariables(self):
        self.master = tkinter.Tk()
        self.master.title("Rock-Paper-Scissors-Spock-Lizard")
        self.master.geometry('1024x683+50+50')
        self.master.resizable(width=tkinter.FALSE, height=tkinter.FALSE)
        self.width  = 1024
        self.height = 683
        self.result = ""


    def loadImages(self):
        self.img01 = tkinter.PhotoImage(data=images.img01)
        self.img02 = tkinter.PhotoImage(data=images.img02)
        self.img01_ws = tkinter.PhotoImage(data=images.img01_ws)
        self.img01_hs  = tkinter.PhotoImage(data=images.img01_hs)
        self.img01_hs1 = tkinter.PhotoImage(data=images.img01_hs1)
        self.img01_abs = tkinter.PhotoImage(data=images.img01_abs)

        self.backSmallBPhoto  = tkinter.PhotoImage(data=images.backSmallBPhoto)
        self.nextSmallBPhoto  = tkinter.PhotoImage(data=images.nextSmallBPhoto)
        self.prevSmallBPhoto  = tkinter.PhotoImage(data=images.prevSmallBPhoto)
        self.startBPhoto      = tkinter.PhotoImage(data=images.startBPhoto)
        self.optionsBPhoto    = tkinter.PhotoImage(data=images.optionsBPhoto)
        self.exitBPhoto       = tkinter.PhotoImage(data=images.exitBPhoto)
        self.helpBPhoto       = tkinter.PhotoImage(data=images.helpBPhoto)
        self.aboutBPhoto      = tkinter.PhotoImage(data=images.aboutBPhoto)
        self.largeBackBPhoto  = tkinter.PhotoImage(data=images.largeBackBPhoto)
        self.setRPGBPhoto     = tkinter.PhotoImage(data=images.setRPGBPhoto)
        self.resultBackBPhoto = tkinter.PhotoImage(data=images.resultBackBPhoto)
        self.playAgainBPhoto  = tkinter.PhotoImage(data=images.playAgainBPhoto)

        self.botStartBox_gs  = tkinter.PhotoImage(data=images.botStartBox_gs)
        self.buttonphoto1_gs = tkinter.PhotoImage(data=images.buttonphoto1_gs)
        self.buttonphoto2_gs = tkinter.PhotoImage(data=images.buttonphoto2_gs)
        self.buttonphoto3_gs = tkinter.PhotoImage(data=images.buttonphoto3_gs)
        self.buttonphoto4_gs = tkinter.PhotoImage(data=images.buttonphoto4_gs)
        self.buttonphoto5_gs = tkinter.PhotoImage(data=images.buttonphoto5_gs)

        self.botphoto1_gs = tkinter.PhotoImage(data=images.botphoto1_gs)
        self.botphoto2_gs = tkinter.PhotoImage(data=images.botphoto2_gs)
        self.botphoto3_gs = tkinter.PhotoImage(data=images.botphoto3_gs)
        self.botphoto4_gs = tkinter.PhotoImage(data=images.botphoto4_gs)
        self.botphoto5_gs = tkinter.PhotoImage(data=images.botphoto5_gs)
        self.botPhotos = [self.botphoto1_gs, self.botphoto2_gs,
                          self.botphoto3_gs, self.botphoto4_gs, self.botphoto5_gs]
        self.messageBox_gs = tkinter.PhotoImage(data=images.messageBox_gs)
        self.botWinPhoto_rs   = tkinter.PhotoImage(data=images.botWinPhoto_rs)
        self.humanWinPhoto_rs = tkinter.PhotoImage(data=images.humanWinPhoto_rs)
        self.drawPhoto_rs     = tkinter.PhotoImage(data=images.drawPhoto_rs)


    def createWidgets(self):
        self.mainGui()
        self.createWelcomeScreen()
        self.createOptionsScreen()
        self.createHelpScreen()
        self.createHelpScreen1()
        self.createAboutScreen()
        self.createRPGScreen()
        self.createGameScreen()
        self.createResultScreen()


    ## @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ###########################################################################
    ## CALLBACKS ##############################################################
    ###########################################################################
    ## @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    def choiceCallback(self, choice):
        """
        Used to send choice to the classifier.
        """
        self.rpssl.playGame(choice)

        # Update canvas with image of bot's choice
        self.botChoiceCanvas_gs.create_image(0, 0, anchor=tkinter.NW,
                              image=self.botPhotos[self.rpssl.playerTwoGuess])
        self.botChoiceCanvas_gs.place(x=460, y=241)

        # Update scores on labels
        self.botLabel_gs.config(text=str(self.rpssl.playerTwoScore))

        self.humanLabel_gs.config(text=str(self.rpssl.playerOneScore))

        self.messageLabel_gs.config(text=self.rpssl.winString)

        if self.rpssl.roundsPlayed == self.rpssl.maxRounds:
            self.result = self.rpssl.getGameResult()
            self.hideGameScreen(0)
            self.label_rsl.config(text=self.result)
            if self.result[0]=="B":
                self.winImageCanvas_rs.create_image(0, 0, anchor=tkinter.NW,
                              image=self.botWinPhoto_rs)
            elif self.result[0]=="P":
                self.winImageCanvas_rs.create_image(0, 0, anchor=tkinter.NW,
                              image=self.humanWinPhoto_rs)
            else:
                self.winImageCanvas_rs.create_image(0, 0, anchor=tkinter.NW,
                              image=self.drawPhoto_rs)               
            self.showResultScreen()
            self.rpssl.initCurrentGameVars()


    def startGame(self, n):
        """
        Clear the current screen widgets and show the game screen ones.
        """
        self.messageLabel_gs.configure(text="Choose your weapon.")
        if n==1:
            self.hideWelcomeScreen()
            self.rpssl.startGame()
            self.showGameScreen()
        if n==2:
            self.hideResultScreen()
            self.rpssl.startGame()
            self.botLabel_gs.config(text="0")
            self.humanLabel_gs.config(text="0")
            self.showGameScreen()  


    def quitApplication(self):
        """
        Close the window and exit the program.
        """
        self.rpssl.saveOnQuit()
        self.master.destroy()
        exit()


    def optionsCallback(self):
        """
        Hide the welcome screen widgets and show the options screen ones.
        """
        self.hideWelcomeScreen()
        self.showOptionsScreen()


    def helpCallback(self):
        """
        Hide the options screen widgets and show the help screen ones.
        """
        self.hideOptionsScreen()
        self.showHelpScreen()


    def aboutCallback(self):    ############################################################
        """
        Hide the options screen widgets and show the help screen ones.
        """
        self.hideOptionsScreen()
        self.showAboutScreen()


    def setRPGCallback(self):
        """
        Hide the option screen widgets and show the set rounds per game screen ones.
        """
        self.hideOptionsScreen()
        self.showRPGScreen()


    def backCallback(self, n):
        """
        Hide current screen widgets and show the welcome screen ones.
        """
        if n==1:
            self.hideOptionsScreen()
        elif n==2:
            self.hideHelpScreen()
        elif n==3:
            self.hideHelpScreen1()
        elif n==4:
            self.hideAboutScreen()
        elif n==5:
            self.rpssl.changeMaxRounds(int(self.spinbox_rpgs.get()))
            self.hideRPGScreen()
        elif n==6:
            self.rpssl.initCurrentGameVars()
            # Update scores on labels
            self.botLabel_gs.config(text="0")
            self.humanLabel_gs.config(text="0")
            self.hideGameScreen(1)
        elif n==7:
            self.rpssl.initCurrentGameVars()
            # Update scores on labels
            self.botLabel_gs.config(text="0")
            self.humanLabel_gs.config(text="0")
            self.hideResultScreen()

        if n in [2,3,4,5]:
            self.showOptionsScreen()
        else:
            self.showWelcomeScreen()


    def nextCallback(self):
        """
        Hide the help screen widgets and show the help screen1 ones.
        """
        self.hideHelpScreen()
        self.showHelpScreen1()


    def prevCallback(self):
        """
        Hide the help screen1 widgets and show the help screen ones.
        """
        self.hideHelpScreen1()
        self.showHelpScreen()
        

    ###########################################################################
    ## GUI BACKGROUND #########################################################

    def mainGui(self):
        """
        Add the background image and logo to the window.
        """
        ## BACKGROUND IMAGE ###################################################
        self.canvas = tkinter.Canvas(self.master, width=self.width, height=self.height,
                        borderwidth=0, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.img01)

        ## LOGO IMAGE #########################################################
        self.canvas1 = tkinter.Canvas(self.canvas, width=255, height=65,
                                       borderwidth=0, highlightthickness=0)
        self.canvas1.place(x=380, y=130)
        self.canvas1.create_image(0,0,anchor=tkinter.NW, image=self.img02)


    ## @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ###########################################################################
    ## GAME SCREENS ###########################################################
    ###########################################################################
    ## @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    ###########################################################################
    ## WELCOME SCREEN #########################################################

    def createWelcomeScreen(self):
        """
        Create the welcome screen widgets.
        """
        #######################################################################
        ## GAME RULES IMAGE ###################################################
        self.canvas1_ws = tkinter.Canvas(self.canvas, width=220, height=211,
                                       borderwidth=0, highlightthickness=0)
        self.canvas1_ws.create_image(0, 0, anchor=tkinter.NW, image=self.img01_ws)

        #######################################################################
        ## BUTTONS ############################################################

        ## START BUTTON #######################################################       
        self.button1_ws = tkinter.Button(self.canvas, compound=tkinter.TOP, width=74,
                         height=44, image=self.startBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command=lambda: self.startGame(1))

        ## OPTIONS BUTTON #####################################################
        self.button2_ws = tkinter.Button(self.canvas, compound=tkinter.TOP, width=94,
                         height=44, image=self.optionsBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command=self.optionsCallback)


        ## EXIT BUTTON ########################################################
        self.button3_ws = tkinter.Button(self.canvas, compound=tkinter.TOP, width=74,
                         height=44, image=self.exitBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command=self.quitApplication)


    def showWelcomeScreen(self):
        """
        Add the welcome screen to the main gui.
        """
        self.canvas1_ws.place(x=396, y=225)
        self.button1_ws.place(x=370, y=525)
        self.button2_ws.place(x=454, y=525)
        self.button3_ws.place(x=558, y=525)


    def hideWelcomeScreen(self):
        """
        Remove the widgets that make the welcome screen
        """
        self.canvas1_ws.place_forget()
        self.button1_ws.place_forget()
        self.button2_ws.place_forget()
        self.button3_ws.place_forget()


    ###########################################################################
    ## OPTIONS SCREEN #########################################################

    def createOptionsScreen(self):
        """
        Create the options screen widgets.
        """
        self.titleLabel_os = tkinter.Label(self.canvas, text="OPTIONS", width=8, 
                            font=("sans",20), bg="white", justify=tkinter.CENTER)


        ## SET RPG BUTTON #####################################################
        self.button1_os = tkinter.Button(self.canvas, compound=tkinter.TOP, width=242,
                         height=68, image=self.setRPGBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command=self.setRPGCallback)

        ## HELP BUTTON ########################################################
        self.button2_os = tkinter.Button(self.canvas, compound=tkinter.TOP, width=242,
                         height=64, image=self.helpBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command=self.helpCallback)

        ## ABOUT BUTTON ######################################################
        self.button3_os = tkinter.Button(self.canvas, compound=tkinter.TOP, width=242,
                         height=64, image=self.aboutBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command=self.aboutCallback)

        ## BACK BUTTON #######################################################
        self.button4_os = tkinter.Button(self.canvas, compound=tkinter.TOP, width=242,
                         height=44, image=self.largeBackBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command = lambda: self.backCallback(1))


    def showOptionsScreen(self):
        """
        Add the options screen to the main gui.
        """
        self.titleLabel_os.place(x=440, y=196)
        self.button1_os.place(x=379, y=254)
        self.button2_os.place(x=379, y=344)
        self.button3_os.place(x=379, y=430)
        self.button4_os.place(x=379, y=525)


    def hideOptionsScreen(self):
        """
        Remove the widgets that make the welcome screen
        """
        self.titleLabel_os.place_forget()
        self.button1_os.place_forget()
        self.button2_os.place_forget()
        self.button3_os.place_forget()
        self.button4_os.place_forget()


    ###########################################################################
    ## HELP SCREEN ############################################################

    def createHelpScreen(self):
        """
        Create the widgets for the help screen.
        """
        ## HELP IMAGE #########################################################        
        self.canvas1_hs = tkinter.Canvas(self.canvas, width=272, height=345,
                                       borderwidth=0, highlightthickness=0)
        self.canvas1_hs.create_image(0, 0, anchor=tkinter.NW, image=self.img01_hs)

        ## NEXT BUTTON ########################################################
        self.button1_hs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=116,
                         height=41, image=self.nextSmallBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command=self.nextCallback)

        ## BACK BUTTON ########################################################
        self.button2_hs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=116,
                         height=41, image=self.backSmallBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command = lambda: self.backCallback(2))


    def showHelpScreen(self):
        """
        Add the help screen widgets to the main gui.
        """
        self.canvas1_hs.place(x=368, y=205)
        self.button1_hs.place(x=378, y=525)
        self.button2_hs.place(x=508, y=525)


    def hideHelpScreen(self):
        """
        Remove the widgets that make the help screen
        """
        self.canvas1_hs.place_forget()
        self.button1_hs.place_forget()
        self.button2_hs.place_forget()


    ###########################################################################
    ## HELP SCREEN1 ###########################################################

    def createHelpScreen1(self):
        """
        Create the widgets for help screen 1.
        """
        ## HELP IMAGE #########################################################        
        self.canvas1_hs1 = tkinter.Canvas(self.canvas, width=272, height=345,
                                       borderwidth=0, highlightthickness=0)
        self.canvas1_hs1.create_image(0, 0, anchor=tkinter.NW, image=self.img01_hs1)

        ## PREV BUTTON ########################################################
        self.button1_hs1 = tkinter.Button(self.canvas, compound=tkinter.TOP, width=116,
                         height=41, image=self.prevSmallBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command=self.prevCallback)

        ## BACK BUTTON ########################################################
        self.button2_hs1 = tkinter.Button(self.canvas, compound=tkinter.TOP, width=116,
                         height=41, image=self.backSmallBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command = lambda: self.backCallback(3))


    def showHelpScreen1(self):
        """
        Add the help screen1 widgets to the main gui.
        """
        self.canvas1_hs1.place(x=368, y=205)
        self.button1_hs1.place(x=378, y=525)
        self.button2_hs1.place(x=508, y=525)


    def hideHelpScreen1(self):
        """
        Remove the widgets that make the help screen
        """
        self.canvas1_hs1.place_forget()
        self.button1_hs1.place_forget()
        self.button2_hs1.place_forget()

    ###########################################################################
    ## ABOUT SCREEN ###########################################################

    def createAboutScreen(self):
        """
        Create the widgets for about screen.
        """
        ## ABOUT IMAGE ########################################################        
        self.canvas1_abs = tkinter.Canvas(self.canvas, width=272, height=320,
                                       borderwidth=0, highlightthickness=0)
        self.canvas1_abs.create_image(0, 0, anchor=tkinter.NW, image=self.img01_abs)

        ## BACK BUTTON #######################################################
        self.button_abs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=242,
                         height=44, image=self.largeBackBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command = lambda: self.backCallback(4)) ########


    def showAboutScreen(self):
        """
        Add the about screen widgets to the main gui.
        """
        self.canvas1_abs.place(x=368, y=205)
        self.button_abs.place(x=379, y=525)


    def hideAboutScreen(self):
        """
        Remove the widgets that make the about screen
        """
        self.canvas1_abs.place_forget()
        self.button_abs.place_forget()


    ###########################################################################
    ## CHANGE ROUNDS PER GAME SCREEN ##########################################

    def createRPGScreen(self):
        """
        Create the rounds per game screen widgets.
        """
        ## TITLE LABEL ########################################################
        self.titleLabel_rpgs = tkinter.Label(self.canvas,
                text="SET NUMBER OF ROUNDS PER GAME", width=18, wraplength=180,
                font=("sans",14), bg="white", justify=tkinter.CENTER)

        ## SPINBOX ############################################################

        ## Default value / value in spinbox
        var = tkinter.StringVar(self.canvas)
        var.set(str(self.rpssl.maxRounds))

        self.spinbox_rpgs = tkinter.Spinbox(self.canvas, bg="white", from_=1, to=99,
                increment=1, textvariable=var, width=3, font=("sans",40),
                justify=tkinter.CENTER)

        ## BACK BUTTON ########################################################
        self.button1_rpgs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=242,
                         height=44, image=self.largeBackBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command = lambda: self.backCallback(5))


    def showRPGScreen(self):
        """
        Add the rounds per game screen to the main gui.
        """
        self.titleLabel_rpgs.place(x=404, y=196)
        self.spinbox_rpgs.place(x=438, y=270)
        self.button1_rpgs.place(x=379, y=525)


    def hideRPGScreen(self):
        """
        Remove the widgets that make the rounds per game screen
        """
        self.titleLabel_rpgs.place_forget()
        self.spinbox_rpgs.place_forget()
        self.button1_rpgs.place_forget()


    ###########################################################################
    ## GAME SCREEN ############################################################

    def createGameScreen(self):
        """
        Create the game screen widgets.
        """
        ## BOT VS HUMAN LABEL #################################################
        self.headerlabel_gs = tkinter.Label(self.canvas, text="ROBOT  vs  HUMAN",
                        font=("sans",20), bg="white", justify=tkinter.CENTER)

        ## SCORE LABELS #######################################################
        self.botLabel_gs = tkinter.Label(self.canvas, text=str(self.rpssl.playerTwoScore),
              width=3, font=("sans",30), bg="white", justify=tkinter.CENTER)

        self.humanLabel_gs = tkinter.Label(self.canvas, text=str(self.rpssl.playerOneScore),
              width=3, font=("sans",30), bg="white", justify=tkinter.CENTER)

        ## BOT CHOICE IMAGE ###################################################
        self.botChoiceCanvas_gs = tkinter.Canvas(self.canvas, width=84, height=84,
                                       borderwidth=0, highlightthickness=0)

        self.botChoiceCanvas_gs.create_image(0, 0, anchor=tkinter.NW,
                              image=self.botStartBox_gs)

        self.botchoiceLabel_gs = tkinter.Label(self.canvas, text="BOT CHOICE", 
                                font=("sans",10), bg="white", justify=tkinter.CENTER)

        ## PLAYER CHOICE BUTTONS ##############################################
        self.button1_gs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=50,
                            height=50, image=self.buttonphoto1_gs, overrelief=tkinter.SUNKEN,
                            padx=0, pady=0, command = lambda: self.choiceCallback("ro"))
        self.label1_gsb = tkinter.Label(self.canvas, text="RO",
                        font=("sans",12), bg="white", justify=tkinter.CENTER)

        self.button2_gs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=50,
                            height=50, image=self.buttonphoto2_gs, overrelief=tkinter.SUNKEN,
                            padx=0, pady=0, command = lambda: self.choiceCallback("pa"))
        self.label2_gsb = tkinter.Label(self.canvas, text="PA",
                        font=("sans",12), bg="white", justify=tkinter.CENTER)

        self.button3_gs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=50,
                            height=50, image=self.buttonphoto3_gs, overrelief=tkinter.SUNKEN,
                            padx=0, pady=0, command = lambda: self.choiceCallback("sc"))
        self.label3_gsb = tkinter.Label(self.canvas, text="SC",
                        font=("sans",12), bg="white", justify=tkinter.CENTER)

        self.button4_gs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=50,
                            height=50, image=self.buttonphoto4_gs, overrelief=tkinter.SUNKEN,
                            padx=0, pady=0, command = lambda: self.choiceCallback("sp"))
        self.label4_gsb = tkinter.Label(self.canvas, text="SP",
                        font=("sans",12), bg="white", justify=tkinter.CENTER)

        self.button5_gs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=50,
                            height=50, image=self.buttonphoto5_gs, overrelief=tkinter.SUNKEN,
                            padx=0, pady=0, command = lambda: self.choiceCallback("li"))
        self.label5_gsb = tkinter.Label(self.canvas, text="LI",
                        font=("sans",12), bg="white", justify=tkinter.CENTER)

        ## MESSAGE BOX ########################################################
        self.messageCanvas_gs = tkinter.Canvas(self.canvas, width=248, height=74,
                                       borderwidth=0, highlightthickness=0)                       
        self.messageCanvas_gs.create_image(0, 0, anchor=tkinter.NW,
                              image=self.messageBox_gs)

        self.messageLabel_gs = tkinter.Label(self.canvas, text="Choose your weapon.", 
                wraplength=220, width=28, font=("sans",10), bg="white", justify=tkinter.CENTER)

        #######################################################################
        ## BOTTOM BUTTONS #####################################################

        ## BACK BUTTON #######################################################
        self.button6_gs = tkinter.Button(self.canvas, compound=tkinter.TOP, width=242,
                         height=44, image=self.largeBackBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command = lambda: self.backCallback(6))


    def showGameScreen(self):
        """
        Add the game screen widgets to the main gui.
        """
        self.headerlabel_gs.place(x=384, y=190)
        self.botLabel_gs.place(x=387, y=220)
        self.humanLabel_gs.place(x=545, y=220)

        ## Put empty box onscreen at the start of each game
        self.botChoiceCanvas_gs.create_image(0, 0, anchor=tkinter.NW,
                              image=self.botStartBox_gs)
        self.botChoiceCanvas_gs.place(x=460, y=241)

        self.botchoiceLabel_gs.place(x=462, y=325)
        self.button1_gs.place(x=366, y=355)
        self.button2_gs.place(x=421, y=355)
        self.button3_gs.place(x=475, y=355)
        self.button4_gs.place(x=530, y=355)
        self.button5_gs.place(x=585, y=355)
        self.label1_gsb.place(x=381, y=410)
        self.label2_gsb.place(x=437, y=410)
        self.label3_gsb.place(x=492, y=410)
        self.label4_gsb.place(x=547, y=410)
        self.label5_gsb.place(x=604, y=410)
        self.messageCanvas_gs.place(x=380, y=440)
        self.messageLabel_gs.place(x=390, y=460)
        self.button6_gs.place(x=379, y=525)


    def hideGameScreen(self, n):
        """
        Hide game screen widgets.
        """
        self.headerlabel_gs.place_forget()
        self.botLabel_gs.place_forget()
        self.humanLabel_gs.place_forget()
        self.botChoiceCanvas_gs.place_forget()
        self.botchoiceLabel_gs.place_forget()
        self.button1_gs.place_forget()
        self.button2_gs.place_forget()
        self.button3_gs.place_forget()
        self.button4_gs.place_forget()
        self.button5_gs.place_forget()
        self.label1_gsb.place_forget()
        self.label2_gsb.place_forget()
        self.label3_gsb.place_forget()
        self.label4_gsb.place_forget()
        self.label5_gsb.place_forget()
        if n:
            self.messageCanvas_gs.place_forget()
            self.messageLabel_gs.place_forget()
        self.button6_gs.place_forget()


    ###########################################################################
    ## RESULTS SCREEN #########################################################

    def createResultScreen(self):
        """
        Create the result screen widgets.
        """
        ## Create the result label
        self.label_rsl = tkinter.Label(self.canvas, text="", width=22,
                        font=("sans",12), bg="white", justify=tkinter.CENTER)

        ## WIN IMAGE ##########################################################
        self.winImageCanvas_rs = tkinter.Canvas(self.canvas, width=212, height=132,
                                       borderwidth=0, highlightthickness=0)

        self.winImageCanvas_rs.create_image(0, 0, anchor=tkinter.NW,
                              image=self.drawPhoto_rs)

        ## PLAY AGAIN BUTTON ##################################################       
        self.button1_rsb = tkinter.Button(self.canvas, compound=tkinter.TOP, width=134,
                         height=44, image=self.playAgainBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command=lambda: self.startGame(2))

        ## BACK BUTTON ########################################################
        self.button2_rsb = tkinter.Button(self.canvas, compound=tkinter.TOP, width=98,
                         height=44, image=self.resultBackBPhoto, overrelief=tkinter.SUNKEN,
                         padx=1, pady=1, command = lambda: self.backCallback(7))


    def showResultScreen(self):
        """
        Add the result screen to the main gui.
        """
        self.label_rsl.place(x=407, y=214)
        self.winImageCanvas_rs.place(x=400,y=280)
        self.button1_rsb.place(x=378, y=525)
        self.button2_rsb.place(x=526, y=525)


    def hideResultScreen(self):
        """
        Remove the widgets that make the result screen
        """
        self.label_rsl.place_forget()
        self.button1_rsb.place_forget()
        self.button2_rsb.place_forget()
        self.messageCanvas_gs.place_forget()
        self.messageLabel_gs.place_forget()
        self.winImageCanvas_rs.place_forget()


if __name__ == "__main__":
    ## Create an instance of the RPSSL class
    if path.isfile("conf/rpssl.pk"):
        rpsslInstance = rpssl.RPSSL(loadPk=1)
    else:
        rpsslInstance = rpssl.RPSSL()

    ## Create the GUI
    GUI = RPSSLGui(rpsslInstance)
    GUI.master.mainloop()

