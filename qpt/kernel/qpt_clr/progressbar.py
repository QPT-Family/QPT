# Author: Acer Zhang
# Datetime:2021/6/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

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


class MainWindow(Window):

    def __init__(self):
        Window.__init__(self)

        # dynamically create page from XAML
        xaml = """
    <Page
      xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
      xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
      <Grid Margin="0,0,2,-1">
        <ProgressBar Margin="10,10,65,10"/>
        <TextBox TextWrapping="Wrap" Text="100%" HorizontalAlignment="Right" HorizontalContentAlignment="Center" VerticalContentAlignment="Center" RenderTransformOrigin="0.489,1.111" Width="64" Background="{x:Null}" BorderThickness="0"/>
    </Grid>
    </Page>
    """
        page = XamlReader.Parse(xaml)

        # # connect Button1
        # self.Button1 = LogicalTreeHelper.FindLogicalNode(page, "Button1")
        # self.Button1.Click += self.Button1_Click
        #
        # # connect Button2
        # self.Button2 = LogicalTreeHelper.FindLogicalNode(page, "Button2")
        # self.Button2.Click += self.Button2_Click

        # set main window properties, and install the page
        self.Title = "Python WPF App with XAML!"
        self.Width = 450
        self.Height = 68
        self.Content = page

    # def Button1_Click(self, sender, e):
    #     MessageBox.Show(self.Button1.Content + " is clicked!")
    #
    # def Button2_Click(self, sender, e):
    #     MessageBox.Show(self.Button2.Content + " is clicked!")


def STAMain():
    app = Application()
    app.Run(MainWindow())


def main():
    t = Thread(ThreadStart(STAMain))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()


if __name__ == "__main__":
    main()
