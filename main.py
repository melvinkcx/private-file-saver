import wx

if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="Secret Bucket")
    frame.Center()

    # Menu bar
    menu_bar = wx.MenuBar()

    # File menu
    file_menu = wx.Menu()
    sign_in_item = file_menu.Append(wx.ID_ANY, 'Sig&n In to AWS', 'Sign In')
    quit_item = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
    frame.Bind(wx.EVT_MENU, lambda e: frame.Close(), quit_item)
    frame.Bind(wx.EVT_MENU, lambda e: print('sign in'), sign_in_item)

    # About menu
    about_menu = wx.Menu()
    about_item = about_menu.Append(wx.ID_ABOUT, '&About App', 'About application')
    frame.Bind(wx.EVT_MENU, lambda e: print('about app'), about_item)

    menu_bar.Append(file_menu, '&File')
    menu_bar.Append(about_menu, '&About')

    frame.SetMenuBar(menu_bar)

    # Status bar
    status_bar = frame.CreateStatusBar()
    status_bar.SetStatusText('[STATUS] Not signed in yet')
    status_bar.Show()

    # Toolbar
    toolbar = frame.CreateToolBar()
    # quit_tool_item = toolbar.AddTool(wx.ID_ANY, 'Quit', wx.Bitmap(''))
    toolbar.Realize()
    # frame.Bind(wx.EVT_TOOL, lambda e: frame.Close(), quit_tool_item)

    frame.Show()

    app.MainLoop()
