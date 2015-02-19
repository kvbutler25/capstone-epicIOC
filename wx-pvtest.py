import wx, epics, epics.wx


class PVFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, -1, title=title, size=(600,120))
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		PV1 = PVPanel(self)
		PV2 = PVPanel(self)

		sizer.Add(PV1, 0, wx.EXPAND)
		sizer.Add(PV2, 0, wx.EXPAND)

		self.SetSizer(sizer)
		self.Show(True)		


class PVPanel(wx.Panel):	
	def __init__(self, parent):
		self.i = 2		
		self.name = 'baseball'		
		wx.Panel.__init__(self, parent, -1, size=(590, 60))
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)		
		
		self.pvName = wx.TextCtrl(self, -1, 'Enter PV name', size=(175,-1), style=wx.TE_PROCESS_ENTER)
		equals = wx.StaticText(self, -1, "=")
		self.pvValue = epics.wx.PVText(self, pv=self.name, font=None, fg=None, bg=None, minor_alarm="DARKRED", major_alarm="RED", invalid_alarm="ORANGERED", auto_units=False, units="")

		self.pvName.Bind(wx.EVT_TEXT_ENTER, self.OnEnter) 				

		self.sizer.Add(self.pvName, 2, wx.EXPAND)
		self.sizer.Add(equals, 1, wx.EXPAND)
		self.sizer.Add(self.pvValue, 2, wx.EXPAND)

		self.SetSizer(self.sizer)
		self.Show(True)
	def OnEnter(self, e):	
		name = self.pvName.GetValue()
		self.name = name
		self.sizer.Hide(self.i)
		self.i+=1
		pvValue = epics.wx.PVText(self, pv=self.name, font=None, fg=None, bg=None, minor_alarm="DARKRED", major_alarm="RED", invalid_alarm="ORANGERED", auto_units=False, units="")
		self.sizer.Add(pvValue, 2, wx.EXPAND)
		self.sizer.Layout()
		self.Fit()


class PVApp(wx.App):
	def OnInit(self):
		frame = PVFrame(None, -1, "Read PV values")
		self.SetTopWindow(frame)
		return True

app = PVApp(0)
app.MainLoop()


