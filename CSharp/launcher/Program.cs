using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;

// Debug需要修改UseShellExecute和ConsoleHelper.hideConsole();
namespace QPTLauncher
{
    class Program
    {
        static void Main(string[] args)
        {
            //ConsoleHelper.hideConsole();
            Process p = new Process();
            Console.Title = "Debug";
            Console.WriteLine("传入参数为：" + args);

            string launcherPath = Environment.CurrentDirectory;
            Console.WriteLine("当前目录为：" + launcherPath);

            string python_file_path = Path.Combine(launcherPath, @"Python/python.exe");
            p.StartInfo.FileName = python_file_path;
            if (!File.Exists(python_file_path))
            {
                ConsoleHelper.showConsole();
                Console.WriteLine("未找到Python解释器，程序运行失败" );
                Console.ReadKey();
            }
            p.StartInfo.Arguments = "-c " + "\"import sys\n" +
                "sys.path.append('./Python')\n" +
                "sys.path.append('./Python/Lib/site-packages')\n" +
                "sys.path.append('./Python/Scripts')\n" +
                "import qpt.run as run\n\"";
            p.StartInfo.UseShellExecute = false;
            //p.StartInfo.UseShellExecute = true;
            p.StartInfo.CreateNoWindow = false;
            p.Start();
            p.WaitForExit();
            Console.ReadKey();
            ////获取cmd窗口的输出信息
            //string result = p.StandardOutput.ReadToEnd();
            //p.WaitForExit();//等待程序执行完退出进程
            //p.Close();
            //Console.WriteLine(result);
            //Console.ReadKey();
        }
    }
}


public static class ConsoleHelper
{
    [System.Runtime.InteropServices.DllImport("user32.dll", SetLastError = true)]
    private static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

    [DllImport("user32.dll", SetLastError = true)]
    private static extern bool ShowWindow(IntPtr hWnd, uint nCmdShow);
    public static void hideConsole(string ConsoleTitle = "")
    {
        ConsoleTitle = String.IsNullOrEmpty(ConsoleTitle) ? Console.Title : ConsoleTitle;
        IntPtr hWnd = FindWindow("ConsoleWindowClass", ConsoleTitle);
        if (hWnd != IntPtr.Zero)
        {
            ShowWindow(hWnd, 0);
        }
    }
    public static void showConsole(string ConsoleTitle = "")
    {
        ConsoleTitle = String.IsNullOrEmpty(ConsoleTitle) ? Console.Title : ConsoleTitle;
        IntPtr hWnd = FindWindow("ConsoleWindowClass", ConsoleTitle);
        if (hWnd != IntPtr.Zero)
        {
            ShowWindow(hWnd, 1);
        }
    }
}
