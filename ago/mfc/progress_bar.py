# Author: Acer Zhang
# Datetime:2021/6/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# IDD_PROGRESSBAR_DIALOG DIALOGEX 0, 0, 223, 10
# STYLE DS_SETFONT | DS_FIXEDSYS | DS_CENTER | WS_POPUP | WS_VISIBLE | WS_CAPTION | WS_SYSMENU
# EXSTYLE WS_EX_CLIENTEDGE | WS_EX_APPWINDOW
# CAPTION "初始化QPT程序"
# FONT 9, "MS Shell Dlg", 400, 0, 0x0
# BEGIN
#     CONTROL         "",IDC_PROGRESS1,"msctls_progress32",0x0,0,0,204,10
#     CONTROL         "100%",IDC_STATIC,"Static",SS_LEFTNOWORDWRAP | WS_GROUP,202,1,20,9,WS_EX_RIGHT
# END


import win32ui
import win32con
from pywin.mfc import dialog


class ProgressBar(dialog.Dialog):
    def __init__(self):
        ids = list()
        # 设置MFC基础外观信息
        ids.append(["初始化QPT程序",
                    (0, 0, 223, 10),
                    win32con.DS_SETFONT | win32con.DS_FIXEDSYS | win32con.DS_CENTER | win32con.WS_POPUP |
                    win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU,
                    win32con.WS_EX_CLIENTEDGE | win32con.WS_EX_APPWINDOW,
                    (9, "MS Sans Serif")])
        # ids.append(["CONTROL", None, 1001, (0, 0, 204, 10)])
        # ids.append(["CONTROL", "100%", -1, "Static", win32con.SS_LEFTNOWORDWRAP | win32con.WS_GROUP, (202, 1, 20, 9),
        #             win32con.WS_EX_RIGHT])
        super(ProgressBar, self).__init__(ids)


if __name__ == '__main__':
    a = ProgressBar()
    a.DoModal()
