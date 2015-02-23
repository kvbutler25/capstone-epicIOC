# TODO: Fix window auto-resizing when PV Value length exceeds width of the frame

import wx, epics, epics.wx


class PVFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, -1, title=title, size=(600,120))

		self.numPVFields = 1		
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		add = wx.Button(self, -1, 'Add PV Field')
		remove = wx.Button(self, -1, 'Remove PV Field')
		add.Bind(wx.EVT_BUTTON, self.AddOnClick, add)
		remove.Bind(wx.EVT_BUTTON, self.RemoveOnClick, remove)	
		buttonSizer.Add(add, 1, wx.EXPAND)
		buttonSizer.Add(remove, 1, wx.EXPAND) 
		
		initPVPanel = PVPanel(self, -1)

		self.mainSizer.Add(buttonSizer, 0, wx.EXPAND)
		self.mainSizer.Add(initPVPanel, 0, wx.EXPAND)

		self.SetSizer(self.mainSizer)		
		self.Fit()		
		self.Show(True)		
	def AddOnClick(self, e):				
		self.numPVFields += 1
		self.mainSizer.Add(PVPanel(self, -1), 0, wx.EXPAND)
		self.Fit()		
		self.Layout()
	def RemoveOnClick(self, e):
		if self.numPVFields >= 2:				
			self.mainSizer.Hide(self.numPVFields)			
			self.mainSizer.Remove(self.numPVFields)
			self.numPVFields -= 1			
			self.Fit()			
			self.mainSizer.Layout()			
			self.Layout()

class PVPanel(wx.Panel):	
	def __init__(self, parent, id):		
		wx.Panel.__init__(self, parent=parent, id=id, size=(590, 60))
		self.parent = parent
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)		
		self.pvName = wx.TextCtrl(self, -1, 'Enter PV name', size=(175,-1), style=wx.TE_PROCESS_ENTER)
		equals = wx.StaticText(self, -1, '=')
		self.PVNotFound = wx.StaticText(self, -1, '')
		
		self.pvName.Bind(wx.EVT_TEXT_ENTER, self.OnEnter) 				

		self.sizer.Add(self.pvName, 2, wx.EXPAND)
		self.sizer.Add(equals, 1, wx.EXPAND)
		self.sizer.Add(self.PVNotFound, 2, wx.EXPAND)
		
		self.SetSizer(self.sizer)
		self.Show(True)
	
	def OnEnter(self, e):	
		REPLACEFIELD = 2		
		name = self.pvName.GetValue()	
		pvExists = epics.caget(name)
		if pvExists != None:
			pvValue = epics.wx.PVText(self, pv=name, font=None, fg=None, bg=None, minor_alarm="DARKRED", major_alarm="RED", invalid_alarm="ORANGERED", auto_units=False, units="")
			self.sizer.Hide(REPLACEFIELD)			
			self.sizer.Remove(REPLACEFIELD);			
			self.sizer.Add(pvValue, 2, wx.EXPAND)
		
		else:
			self.sizer.Hide(REPLACEFIELD)			
			self.sizer.Remove(REPLACEFIELD);					
			errMsg = "error: PV %s not found" % name 
			err = wx.StaticText(self,-1, errMsg)
			err.Wrap(200)
			self.sizer.Add(err, 2, wx.EXPAND)
		self.Layout()		
		#self.parent.Fit()

class PVApp(wx.App):
	def OnInit(self):
		frame = PVFrame(None, -1, "Read PV values")
		self.SetTopWindow(frame)
		return True

app = PVApp(0)
app.MainLoop()


