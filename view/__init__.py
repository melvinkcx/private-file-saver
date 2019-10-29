import wx


class AboutDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(vgap=4, hgap=4)

        text = wx.StaticText(panel, label="About Secret Bucket")

        sizer.Add(text, pos=(0, 0))
        panel.SetSizer(sizer)


class Window(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(title="Secret Bucket", *args, **kwargs)

        self.init_ui()
        self.Center()

    def init_ui(self):
        """
        Notes:

        sizer.Add(*, pos=(row, col), **)
        :return:
        """
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(vgap=4, hgap=4)
        text = wx.StaticText(panel, label="Local Files")
        sizer.Add(text,
                  pos=(0, 0),  # Positioning at row 0, col 0 (top left corner)
                  flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10  # Add spaces to top, left, bottom
                  )
        text_ctrl = wx.TextCtrl(panel)
        sizer.Add(text_ctrl,
                  pos=(1, 0),  # Positioning at row 1, col 0
                  span=(1, 5),  # Expanding 1 row and 5 cols
                  flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10
                  )

        button_ok = wx.Button(panel, label="Ok", size=(90, 28))
        button_close = wx.Button(panel, label="Close", size=(90, 28))
        sizer.Add(button_ok, pos=(3, 3))
        sizer.Add(button_close, pos=(3, 4), flag=wx.RIGHT | wx.BOTTOM, border=10)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)

        panel.SetSizer(sizer)

    def add_menu_bar(self):
        # Menu bar
        menu_bar = wx.MenuBar()

        # File menu
        file_menu = wx.Menu()

        # File menu -> Quit
        file_item_quit = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), file_item_quit)

        # Adding file menu
        menu_bar.Append(file_menu, '&File')

        # Edit menu
        edit_menu = wx.Menu()

        # Edit menu -> Settings
        edit_item_settings = edit_menu.Append(wx.ID_ANY, '&Settings', 'App settings')
        self.Bind(wx.EVT_MENU, lambda e: print("setting"), edit_item_settings)

        # Adding edit menu
        menu_bar.Append(edit_menu, '&Edit')

        # About menu
        about_menu = wx.Menu()

        # About menu -> About App
        about_menu_item_about_app = about_menu.Append(wx.ID_ANY, '&About', 'About application')
        self.Bind(wx.EVT_MENU, lambda e: print("about"), about_menu_item_about_app)

        # Adding about menu
        menu_bar.Append(about_menu, '$About')


if __name__ == "__main__":
    app = wx.App()
    window = Window(None)
    window.Show()
    app.MainLoop()
