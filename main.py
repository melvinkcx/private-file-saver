"""
GUI written with wxPython

References:
    - https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
"""
import glob
import os

import wx
import wx.adv

BIN_PATH = os.getcwd()
LOGOS_PATH = f"{BIN_PATH}/images/logos"
ICONS_PATH = f"{BIN_PATH}/images/icons"
TARGET_PATH = '/home/melvin/Project/secret-bucket/target_folder'


def scan_dirs(target_path=TARGET_PATH):
    import glob
    import os
    os.chdir(target_path)
    return glob.glob("**", recursive=False)


class Window(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(title="Secret Bucket", *args, **kwargs)

        self.target_directory = TARGET_PATH

        # self.create_splash_screen()
        self.init_ui()
        self.Center()

    def create_splash_screen(self):
        bitmap = wx.Bitmap(f'{LOGOS_PATH}/bucket_64.png', wx.BITMAP_TYPE_PNG)

        wx.adv.SplashScreen(bitmap=bitmap,
                            splashStyle=wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                            milliseconds=3000,
                            parent=None,
                            id=wx.ID_ANY,
                            pos=wx.DefaultPosition,
                            size=wx.DefaultSize,
                            style=wx.STAY_ON_TOP | wx.BORDER_NONE)

        wx.Yield()

    def init_ui(self):
        """
        Notes:

        sizer.Add(*, pos=(row, col), **)
        :return:
        """
        self.SetIcon(wx.Icon(f'{LOGOS_PATH}/bucket_32.png', wx.BITMAP_TYPE_PNG))

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(vgap=4, hgap=4)
        label = wx.StaticText(panel, label=f"Local Files\nPath: {self.target_directory}")
        sizer.Add(label,
                  pos=(0, 0),  # Positioning at row 0, col 0 (top left corner)
                  flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=10  # Add spaces to top, left, bottom
                  )

        # File list
        file_list = wx.ListCtrl(panel, id=wx.ID_ANY, style=wx.LC_REPORT)
        file_list.InsertColumn(0, 'File')
        file_list.InsertColumn(1, 'Sync?')
        file_list.SetColumnWidth(0, 200)

        # File list: Icon list
        icon_list = glob.glob(f"{ICONS_PATH}/*.png")
        unknown_icon = f"{ICONS_PATH}/unknown.png"
        logo_icon = f"{LOGOS_PATH}/bucket_16.png"

        image_list = wx.ImageList(16, 16)
        image_list.Add(wx.Bitmap(logo_icon))
        # [image_list.Add(wx.Bitmap(icon_path)) for icon_path in icon_list]

        file_list.SetImageList(image_list, wx.IMAGE_LIST_NORMAL)

        file_list.InsertItem(0, '..')
        file_list.SetItemImage(0, 0)

        # File list: File items
        # files = scan_dirs()
        # for file in files[:1]:
        #     index = file_list.InsertItem(len(files), file)
        #     file_list.SetItemImage(index, 0)  # Unknown file icon

        sizer.Add(file_list,
                  pos=(1, 0),
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
                  border=10)

        # Specifies growable col/row when window is resized
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(1)

        panel.SetSizer(sizer)

        self.add_menu_bar()

        self.Bind(wx.EVT_CLOSE, self.on_close_window)

    def on_about_box(self, event):

        description = """
        Private File Saver
        """

        licence = """
        Icon made by Freepik from www.flaticon.com
        Icon made by prettyicon from www.flaticon.com
        """

        info = wx.adv.AboutDialogInfo()

        info.SetIcon(wx.Icon(f'{BIN_PATH}/images/logos/bucket_128.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Private File Saver')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2019 Melvin Koh')
        info.SetWebSite('https://melvinkoh.dev')
        info.SetLicence(licence)
        info.AddDeveloper('Melvin Koh')
        info.AddDocWriter('Melvin Koh')

        wx.adv.AboutBox(info)

    # Event Handlers
    def on_close_window(self, event):
        dialog = wx.MessageDialog(None, 'Are you sure to quit?', "Quit",
                                  style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        ret = dialog.ShowModal()
        if ret == wx.ID_YES:
            self.Destroy()
        else:
            dialog.Hide()

    def add_menu_bar(self):
        # Menu bar
        menu_bar = wx.MenuBar()

        # File menu
        file_menu = wx.Menu()

        # File menu -> Quit
        file_item_quit = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, self.on_close_window, file_item_quit)

        # Adding file menu
        menu_bar.Append(file_menu, '&File')

        # Edit menu
        edit_menu = wx.Menu()

        # Edit menu -> Settings
        edit_item_settings = edit_menu.Append(wx.ID_ANY, '&Settings', 'App settings')
        self.Bind(wx.EVT_MENU, lambda e: print("setting"), edit_item_settings)

        # Adding edit menu
        menu_bar.Append(edit_menu, '&Edit')

        # Help menu
        help_menu = wx.Menu()

        # Help menu -> About App
        help_menu_item_about_app = help_menu.Append(wx.ID_ANY, '&About', 'About application')
        self.Bind(wx.EVT_MENU, self.on_about_box, help_menu_item_about_app)

        # Adding help menu
        menu_bar.Append(help_menu, '&Help')
        self.SetMenuBar(menu_bar)


if __name__ == "__main__":
    app = wx.App()
    window = Window(None)
    window.Show()
    app.MainLoop()
