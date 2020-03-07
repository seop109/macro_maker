import wx
import time
import pathlib
from os import path


MACRO_BAT_FILE_NAME = "run.bat"
MACRO_FILE_NAME = "getwhatyouwant.py"


class AppFrame( wx.Frame ):

    def __init__( self ):

        wx.Frame.__init__( self, None, title="매크로만들기",
                           style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP )
        self.ShowFullScreen(True)
        
        self.alphaValue = 100
        self.SetTransparent( self.alphaValue )      # Easy !

        self.panel = wx.Panel( self )
        self.txt = wx.TextCtrl(self.panel, -1)

        self.timer = wx.Timer(self)
        self.timer.Start(100)
        self.Bind(wx.EVT_TIMER, self.ShowInfo, self.timer)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow )
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)

        self.output_file = pathlib.Path(MACRO_FILE_NAME).absolute()
        if path.exists(self.output_file):
            wx.MessageBox('기존 매크로에 이어서 진행합니다.', 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            dlg = wx.TextEntryDialog(self.panel,
                                 '몇 초 뒤에 매크로가 시작할지 정해주세요.\
                                  \n(기본값 10초):',"입력값","10", 
                style=wx.OK)
            dlg.ShowModal()
            self.txt.SetValue(dlg.GetValue())
            dlg.Destroy()
        
            input_txt = self.txt.GetValue()
            with open(self.output_file, "w") as f:
                f.write("import time\n")
                f.write("import wx\n\n")
                f.write("time.sleep({})\n\n".format(input_txt))

            with open(MACRO_BAT_FILE_NAME, "w") as f:
                f.write("@echo off\n")
                f.write("start /min python %~dp0%{}\n\n".format(MACRO_FILE_NAME))
                

    def ShowInfo(self, event):
        self.timer.Stop()
        resp = wx.MessageBox('매크로를 할 동작을 저장합니다. 순서에 맞게 행동해 주세요.\
                       \n현재는 마우스왼쪽클릭, 텍스트입력만 가능합니다.\
                       \n모든 행동이 끝나면 ESC 키를 눌러서 정상화면으로 돌아가주세요.\
                       \n확인 을 누르면 시작합니다.', 'Info', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
        if resp == wx.CANCEL:
            self.Destroy()

    def OnKey(self, event):
        """
        Check for ESC key press and exit is ESC is pressed
        """
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            wx.MessageBox('매크로 파일을 {} 에 저장하였습니다.\
                           \n매크로 파일을 열어서 세부 수정 후 테스트 바랍니다.\
                           \n매크로 실행방법은 {} 실행해주세요.'.format(MACRO_FILE_NAME, MACRO_BAT_FILE_NAME),
                          'Info', wx.OK | wx.ICON_INFORMATION)

            self.Destroy()            
        else:
            event.Skip()

    def OnCloseWindow( self, evt ) :
        self.Destroy()

    def OnClick(self, event):
        x, y = wx.GetMousePosition()

        dlg = wx.TextEntryDialog(self.panel,
                                 '클릭한 위치에 입력할 값이 있으면 그 값을 쓴 다음 OK를 눌러주세요.\
                                  \n만약 없다면 아무것도 쓰지말고 OK를 눌러주세요.:',"입력값","", 
                style=wx.OK)
        dlg.ShowModal()
        self.txt.SetValue(dlg.GetValue())
        dlg.Destroy()
        input_txt = self.txt.GetValue()
        
        dlg = wx.TextEntryDialog(self.panel,
                                 '다음 매크로 시작하기 전 대기시간을 입력해주세요.\
                                  \n기본값 0.5초.:',"입력값","0.5", 
                style=wx.OK)
        dlg.ShowModal()
        self.txt.SetValue(dlg.GetValue())
        dlg.Destroy()
        input_time = self.txt.GetValue()
        
        if input_txt != '':
            with open(self.output_file, "a") as f:
                f.write("wx.UIActionSimulator().MouseMove({}, {})\n".format(str(x), str(y)))
                f.write("wx.UIActionSimulator().MouseClick(wx.MOUSE_BTN_LEFT)\n")
                f.write("wx.UIActionSimulator().Text('{}')\n".format(str(input_txt)))
                f.write("time.sleep({})\n\n".format(input_time))
        else:
            with open(self.output_file, "a") as f:
                f.write("wx.UIActionSimulator().MouseMove({}, {})\n".format(str(x), str(y)))
                f.write("wx.UIActionSimulator().MouseClick(wx.MOUSE_BTN_LEFT)\n")
                f.write("time.sleep({})\n\n".format(input_time))
        
        event.Skip()

#end AppFrame class

if __name__ == '__main__' :

    app = wx.App( False )
    resp = wx.MessageBox('먼저 매크로를 할 상황을 만들어주세요.\
                         \n매크로를 저장할 상황을 만든 다음에 확인 버튼을 눌러주세요.',
                         'Info', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
    if resp == wx.OK:
        frm = AppFrame()
        frm.Show()
        app.MainLoop()
