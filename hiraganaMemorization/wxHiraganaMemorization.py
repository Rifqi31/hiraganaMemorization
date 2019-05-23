#!/usr/bin/python
# -*- coding: utf-8 -*-
from ConfigParser import RawConfigParser
from os import path
import wx
from evtHandler import statsBtnHandler, changesDictBtnHandler, \
    resetToggleOpt, hideDefinitionHandler, hideSyllableImgHandler, \
    handleClickInputBox, handleInput
from ChangeDictFrame import ChangeDictFrame
from random import choice as randChoice

pathToModule = path.dirname(__file__)
if len(pathToModule) == 0:
    pathToModule = '.'


# add timer?

class MainFrame(wx.Frame):

    def __init__(self):
        self.WindowSize = (1175, 400)
        # use default frame style but disable border resize and maximize
        wx.Frame.__init__(
            self,
            parent=None,
            id=wx.ID_ANY,
            title='Hiragana Memorization',
            size=self.WindowSize,
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX,
        )
        self.unusedDicts = ['test']
        self.currDicts = ['verbs']
        self.cdp = ChangeDictFrame(self, self.unusedDicts,
                                   self.currDicts)

        # self.confParser=RawConfigParser()
        # self.configFile=pathToModule+"/../config.conf"
        # self.confParser.read(self.configFile)

        self.imgBoxSize = (800, 100)
        self.inputTxtSize = (800, 32)
        self.symDictPath = path.join(pathToModule, 'symDicts')
        self.symImgPath = path.join(pathToModule, 'symImg')
        self.currWord = ''
        self.definition = ''
        self.LAST = False

        self.currImgHolder = []
        self.prevImgHolder = []

        self.loadSymDicts()
        self.hideSyllableImgFlag = False

        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.toggleOptSizer = wx.BoxSizer(wx.VERTICAL)

        self.prevImgSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.prevImgNLabelSizer = wx.BoxSizer(wx.VERTICAL)

        self.currImgSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.currImgNLabelSizer = wx.BoxSizer(wx.VERTICAL)

        self.imgBoxSizer = wx.BoxSizer(wx.VERTICAL)

        self.clickableOptSizer = wx.BoxSizer(wx.VERTICAL)

        self.inputTxtSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.addToggleOptions()
        self.addPrevImgBox()
        self.addCurrImgBox()
        self.addInputTxt()
        self.addClickableOptions()

        self.topSizer.Add(self.toggleOptSizer)

        self.imgBoxSizer.Add(self.prevImgNLabelSizer,
                             flag=wx.ALIGN_CENTRE)

        self.imgBoxSizer.AddSpacer(20)

        self.imgBoxSizer.Add(self.currImgNLabelSizer,
                             flag=wx.ALIGN_CENTRE)
        self.imgBoxSizer.Add(self.inputTxtSizer, flag=wx.ALIGN_CENTRE)

        self.topSizer.Add(self.imgBoxSizer, flag=wx.ALIGN_CENTRE)

        self.topSizer.Add(self.clickableOptSizer)

        self.SetSizer(self.topSizer)
        self.Layout()

        self.Bind(wx.EVT_CLOSE, self.closeHandler)

        self.Center()
        self.Show()
        self.cdp.Hide()

    def closeHandler(self, evt=None):
        self.Destroy()

    def loadSymDicts(self):
        temp = {}
        self.wordDict = {}
        for file in self.currDicts:
            d = open(path.join(self.symDictPath,
                     file)).read().replace('\n', '')
            d = d.lower()
            exec 'temp=' + '{' + d + '}'
            self.wordDict.update(temp)

    def addToggleOptions(self):

        self.noneRadio = wx.RadioButton(
            self,
            id=-1,
            label='None',
            style=wx.RB_GROUP
        )
        self.hideSyllableImg = wx.RadioButton(
            self,
            id=-1,
            label='Hide characters'
        )
        self.hideDefinition = wx.RadioButton(
            self,
            id=-1,
            label='Hide definition'
        )

        self.toggleOptSizer.Add(self.noneRadio, proportion=0,
                                flag=wx.ALL, border=20)
        self.toggleOptSizer.Add(self.hideSyllableImg, proportion=0,
                                flag=wx.ALL, border=20)
        self.toggleOptSizer.Add(self.hideDefinition, proportion=0,
                                flag=wx.ALL, border=20)

        self.hideSyllableImg.Bind(
            wx.EVT_RADIOBUTTON,
            lambda evt: hideSyllableImgHandler(self, evt)
        )

        self.hideDefinition.Bind(
            wx.EVT_RADIOBUTTON,
            lambda evt: hideDefinitionHandler(self, evt)
        )

        self.noneRadio.Bind(
            wx.EVT_RADIOBUTTON,
            lambda evt: resetToggleOpt(self, evt)
        )

        tip = 'Hide english definition of the world'
        self.hideDefinition.SetToolTipString(tip)

        tip = 'Hide image syllable of the word'
        self.hideSyllableImg.SetToolTipString(tip)

    def getImage(self, filename):
        img = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        imgRes = wx.StaticBitmap(self, -1, img, (img.GetWidth(),
                                 img.GetHeight()))

        return imgRes

    def drawWord(self, fileList, targSizer, storage, hidden=False):

        for f in fileList:
            imgObj = self.getImage(path.join(self.symImgPath, f))
            if hidden:
                imgObj.Hide()
            storage.append(imgObj)
            targSizer.Add(imgObj, proportion=0, flag=wx.ALL, border=0)

        if self.hideSyllableImgFlag is False:
            [img.Show() for img in storage]

        self.imgBoxSizer.Layout()
        self.Layout()

    def fileListForWord(self, word):
        return [syllable.capitalize() + '.png' for syllable in
                word.split('-')]

    def addCurrImgBox(self):

        self.currWord = randChoice(self.wordDict.keys())
        self.definition = self.wordDict[self.currWord]
        self.wordDict.pop(self.currWord)

        self.currWordLabel = wx.StaticText(self)
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL,
                       wx.FONTWEIGHT_NORMAL)
        self.currWordLabel.SetFont(font)

        fileList = self.fileListForWord(self.currWord)

        self.drawWord(fileList, self.currImgSizer, self.currImgHolder)
        self.currImgNLabelSizer.Add(self.currImgSizer,
                                    flag=wx.ALIGN_CENTRE)

        self.currWordLabel.SetLabel(self.definition)
        self.currImgNLabelSizer.Add(self.currWordLabel,
                                    flag=wx.ALIGN_CENTRE)

    def addPrevImgBox(self):

        self.prevWordLabel = wx.StaticText(self)
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL,
                       wx.FONTWEIGHT_NORMAL)
        self.prevWordLabel.SetFont(font)

        self.prevWordLabel.SetLabel('')
        self.prevImgNLabelSizer.Add(self.prevWordLabel,
                                    flag=wx.ALIGN_CENTRE)

        self.prevImgNLabelSizer.Add(self.prevImgSizer,
                                    flag=wx.ALIGN_CENTRE)

    def addInputTxt(self):
        self.inputTxt = wx.TextCtrl(self, size=self.inputTxtSize,
                                    style=wx.TE_PROCESS_ENTER)
        self.inputTxt.SetValue('Enter syllables')

        self.inputTxt.Bind(
            wx.EVT_TEXT_ENTER,
            lambda evt: handleInput(self, evt)
        )

        self.inputTxt.Bind(
            wx.EVT_KILL_FOCUS,
            lambda evt:
            evt.GetEventObject().SetValue('Enter syllables')
        )

        self.inputTxt.Bind(wx.EVT_LEFT_DOWN, handleClickInputBox)
        self.inputTxt.Bind(wx.EVT_SET_FOCUS, handleClickInputBox)

        self.inputTxt.SetFocus()

        self.inputTxtSizer.Add(self.inputTxt, proportion=0,
                               flag=wx.ALL, border=25)

    def addClickableOptions(self):
        self.statsButton = wx.Button(self, label='View Statistics')
        self.changeDict = wx.Button(self, label='Change dictionary')

        self.clickableOptSizer.Add(self.statsButton, proportion=0,
                                   flag=wx.ALL, border=20)
        self.clickableOptSizer.Add(self.changeDict, proportion=0,
                                   flag=wx.ALL, border=20)

        self.statsButton.Bind(wx.EVT_BUTTON, statsBtnHandler)
        self.changeDict.Bind(
            wx.EVT_BUTTON,
            lambda evt: changesDictBtnHandler(self, evt)
        )


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
