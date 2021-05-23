using System;
using System.Diagnostics;



namespace QPTLauncher
{
    class Program
    {
        static void Main(string[] args)
        {
            Process p = new Process();
            string str1 = System.Environment.CurrentDirectory;
            Console.WriteLine(str1);
            p.StartInfo.FileName = @"C:\Users\GT_BConsole\AppData\Local\Programs\Python\Python37\python.exe";
            Console.WriteLine(args);
            if (args.Length == 0)
            {
                p.StartInfo.Arguments = @"D:\Python_Projects\QPT\qpt\gui\qpt_start.py";
            }
            else
            {
                p.StartInfo.Arguments = @"D:\Python_Projects\QPT\qpt\gui\qpt_start.py " + args[0];
            }

            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.RedirectStandardInput = true;
            p.StartInfo.RedirectStandardError = true;
            p.StartInfo.CreateNoWindow = false;
            p.Start();
            Console.ReadKey();
        }
    }
}
