# Author: Acer Zhang
# Datetime:2021/6/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import time
import clr

clr.AddReference("PresentationFramework.Classic, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
clr.AddReference("PresentationCore, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")

from System.Windows import Application
from System.Windows import Window
from System.Windows import MessageBox
from System.Windows import LogicalTreeHelper
from System.Windows.Markup import XamlReader
from System.Threading import Thread
from System.Threading import ApartmentState
from System.Threading import ThreadStart
from System import *

__all__ = ["MainWindow", "main"]

TITLE = "QPT Initializer - "
KEYS_1 = [60, 59, 63, 18]  # QPT
KEYS_10 = [68, 48, 62, 18]  # YES


class MainWindow(Window):

    def __init__(self):
        Window.__init__(self)
        self.keys = [0, 0, 0, 0]
        xaml = """
    <Page
      xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
      xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
      <Grid Margin="0,0,2,-1">
       <ProgressBar x:Name="progressBar" Margin="10,10,53,10" Value="{Binding Text, ElementName=textBox}"/>
        <TextBox x:Name="textBox" TextWrapping="Wrap" Text="1" HorizontalAlignment="Right" 
        HorizontalContentAlignment="Right" VerticalContentAlignment="Center" RenderTransformOrigin="0.489,1.111" 
        Width="29" Background="{x:Null}" BorderThickness="0" IsEnabled="False" Margin="0,0,19,0"/>
        <Button x:Name="act_button" Content="Button" HorizontalAlignment="Left" Height="25" Margin="7,43,0,-30" 
        VerticalAlignment="Top" Width="87"/>
        <TextBox x:Name="textBox_Copy" TextWrapping="Wrap" Text="%" HorizontalAlignment="Right" 
        VerticalContentAlignment="Center" RenderTransformOrigin="0.489,1.111" Width="18" Background="{x:Null}" 
        BorderThickness="0" IsEnabled="False" Margin="0,0,1,0"/>
    </Grid>
    </Page>
    """
        page = XamlReader.Parse(xaml)

        # connect Button1
        # self.Button1 = LogicalTreeHelper.FindLogicalNode(page, "Button1")
        # self.Button1.Click += self.Button1_Click
        self.Title = TITLE
        self.Width = 450
        self.Height = 68
        self.Content = page
        self.ResizeMode = 0

        self.progressBar = LogicalTreeHelper.FindLogicalNode(page, "progressBar")
        self.text = LogicalTreeHelper.FindLogicalNode(page, "textBox")
        self.btn = LogicalTreeHelper.FindLogicalNode(page, "act_button")
        self.KeyDown += self.b_start

    def add_bar_value(self, add_value: int):
        if self.progressBar.Value + add_value >= 100:
            self.progressBar.Value = 99
        else:
            self.progressBar.Value += add_value

    def set_title(self, text: str):
        self.Title = TITLE + text

    def set_text(self, text: str):
        self.text = text

    def b_start(self, sender, e):
        print(self.keys)
        self.keys.append(e.Key)
        self.keys.pop(0)
        if e.Key == 1:
            print(1)
        if self.keys == KEYS_1:
            self.add_bar_value(1)
        elif self.keys == KEYS_10:
            self.add_bar_value(10)


def sta():
    mw = MainWindow()
    app = Application()
    app.Run(mw)


def main():
    t = Thread(ThreadStart(sta))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()


if __name__ == "__main__":
    main()
