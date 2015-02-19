import wx, epics, epics.wx

app = wx.App()

frame = wx.Frame(None, -1, '')
frame.SetToolTip(wx.ToolTip('This is a frame'))
frame.SetCursor(wx.StockCursor(wx.CURSOR_MAGNIFIER))
frame.SetPosition(wx.Point(0,0))
frame.SetSize(wx.Size(300,250))
frame.SetTitle('PV test')
frame.display = epics.wx.PVTextCtrl(frame, pv='baseball', font=None, fg=None, bg=None, dirty_timeout=1000)
frame.Show()

app.MainLoop()
