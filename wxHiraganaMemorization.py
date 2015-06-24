from ConfigParser import RawConfigParser
from os import path
import wx
from evtHandler import *


pathToModule=path.dirname(__file__)
if len(pathToModule)==0:
	pathToModule='.'


class MainPanel(wx.Panel):

	def __init__(self, parent):
		self.parent=parent
		wx.Panel.__init__(self, parent)

		#self.confParser=RawConfigParser()
		#self.configFile=pathToModule+"/../config.conf"
		#self.confParser.read(self.configFile)
		self.imgBoxSize=(800,100)
		self.inputTxtSize=(800,32)
		self.symDictPath=path.join(pathToModule,"symDicts")
		self.symImgPath=path.join(pathToModule,"symImg")
		self.currWord=""
		self.definition=""

		self.currImgHolder=[]
		self.prevImgHolder=[]
		self.defaultDict=["verbs"]
		self.wordDict=self.loadSymDicts()

		self.topSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.toggleOptSizer = wx.BoxSizer(wx.VERTICAL)


		self.prevImgSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.prevImgNLabelSizer = wx.BoxSizer(wx.VERTICAL)

		self.currImgSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.currImgNLabelSizer = wx.BoxSizer(wx.VERTICAL)

		self.imgBoxSizer= wx.BoxSizer(wx.VERTICAL)

		self.clickableOptSizer = wx.BoxSizer(wx.VERTICAL)

		self.inputTxtSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.addToggleOptions()
		self.addPrevImgBox()
		self.addCurrImgBox()
		self.addInputTxt()
		self.addClickableOptions()

		self.topSizer.Add(self.toggleOptSizer)

		self.imgBoxSizer.Add(self.prevImgNLabelSizer, flag=wx.ALIGN_CENTRE)
		self.imgBoxSizer.Add(self.currImgNLabelSizer, flag=wx.ALIGN_CENTRE)
		self.imgBoxSizer.Add(self.inputTxtSizer, flag=wx.ALIGN_CENTRE)

		self.topSizer.Add(self.imgBoxSizer, flag=wx.ALIGN_CENTRE)

		self.topSizer.Add(self.clickableOptSizer)

		self.SetSizer(self.topSizer)
		self.Layout()

		self.parent.Bind(wx.EVT_CLOSE, self.closeHandler)

	def closeHandler(self,evt=None):
		self.parent.Destroy()

	def loadSymDicts(self):
		wordDict={}
		temp={}

		for file in self.defaultDict:
			d=open( path.join(self.symDictPath,file) ).read().replace("\n","")
			d=d.lower()
			exec("temp="+"{"+d+"}")
			wordDict.update(temp)

		return wordDict

	def addToggleOptions(self):

		self.hideRomaji= wx.CheckBox(parent=self, id=-1, label="Hide romaji")
		self.hideDefinition= wx.CheckBox(parent=self, id=-1, label="Hide definition")

		self.toggleOptSizer.Add(self.hideRomaji, proportion=0, flag=wx.ALL, border=20)
		self.toggleOptSizer.Add(self.hideDefinition, proportion=0, flag=wx.ALL, border=20)

		self.Bind(wx.EVT_CHECKBOX, hideRomajiHandler, self.hideRomaji)
		self.Bind(wx.EVT_CHECKBOX, hideDefinitionHandler, self.hideDefinition)

		tip="Hide english definition of the world"
		self.hideDefinition.SetToolTipString(tip)

		tip="Hide phonetic pronounciation of the word"
		self.hideRomaji.SetToolTipString(tip)

	def getImage(self, filename):
		img = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()

		imgRes=wx.StaticBitmap(self, -1, img, (img.GetWidth(), img.GetHeight()))

		return imgRes

	def drawWord(self, fileList, targSizer, storage, hidden=False):

		for f in fileList:
			imgObj=self.getImage(path.join(self.symImgPath,f))
			if hidden:
				imgObj.Hide()
			storage.append(imgObj)
			targSizer.Add(imgObj, proportion=0, flag=wx.ALL, border=0)

	def fileListForWord(self, word):
		return [syllable.lower()+".png" for syllable in word.split('-')]

	def addCurrImgBox(self):

		self.currWord="ta-be-ma-su"

		self.currWordLabel=wx.StaticText(self)
		font=wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.currWordLabel.SetFont(font)

		self.currWordLabel.SetLabel(self.currWord)
		self.currImgNLabelSizer.Add(self.currWordLabel, flag=wx.ALIGN_CENTRE)

		fileList=self.fileListForWord(self.currWord)

		self.drawWord(fileList, self.currImgSizer, self.currImgHolder)
		self.currImgNLabelSizer.Add(self.currImgSizer, flag=wx.ALIGN_CENTRE)


	def addPrevImgBox(self):

		#placeholder

		word="no-mi-ma-su"

		self.prevWordLabel=wx.StaticText(self)
		font=wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.prevWordLabel.SetFont(font)

		self.prevWordLabel.SetLabel(word)
		self.prevImgNLabelSizer.Add(self.prevWordLabel, flag=wx.ALIGN_CENTRE)

		fileList=self.fileListForWord(word)

		self.drawWord(fileList, self.prevImgSizer, self.prevImgHolder)
		self.prevImgNLabelSizer.Add(self.prevImgSizer, flag=wx.ALIGN_CENTRE)


	def addInputTxt(self):
		self.inputTxt= wx.TextCtrl(self, size=self.inputTxtSize, style=wx.TE_PROCESS_ENTER)
		self.inputTxt.SetValue("Enter syllables")

		self.inputTxt.Bind(wx.EVT_TEXT_ENTER, lambda evt :handleInput(self, evt) )

		self.inputTxt.Bind(wx.EVT_KILL_FOCUS, lambda evt : evt.GetEventObject().SetValue("Enter syllables"))

		self.inputTxt.Bind(wx.EVT_LEFT_DOWN, handleClickInputBox)
		self.inputTxt.Bind(wx.EVT_SET_FOCUS, handleClickInputBox)

		self.inputTxt.SetFocus()

		self.inputTxtSizer.Add(self.inputTxt, proportion=0, flag=wx.ALL, border=25)


	def addClickableOptions(self):
		self.statsButton=wx.Button(self, label="View Statistics")
		self.changeDict=wx.Button(self, label="Change dictionary")

		self.clickableOptSizer.Add(self.statsButton ,proportion=0, flag=wx.ALL, border=20)
		self.clickableOptSizer.Add(self.changeDict,proportion=0, flag=wx.ALL, border=20)

		self.statsButton.Bind(wx.EVT_BUTTON, statsBtnHandler)
		self.changeDict.Bind(wx.EVT_BUTTON, changesDictBtnHandler)


class MainFrame(wx.Frame):
	def __init__(self):
		self.WindowSize=(1175,400)
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="Hiragana Memorization", size=self.WindowSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)#use default frame style but disable border resize and maximize

		self.mp=MainPanel(self)
		self.Center()
		self.Show()


if __name__ == "__main__":
	app = wx.App(False)
	frame = MainFrame()
	frame.Show()
	app.MainLoop()