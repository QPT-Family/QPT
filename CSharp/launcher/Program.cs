using System;
using System.Diagnostics;
using System.IO;

namespace QPTLauncher
{
    class Program
    {
        static void Main(string[] args)
        {
            Process p = new Process();

            Console.WriteLine("传入参数为："+args);

            string launcherPath = Environment.CurrentDirectory;
            Console.WriteLine("当前目录为：" + launcherPath);

            // [1kb QPT支持] ToDO 增加QPT_HOME检测

            // 常规启动方式
            if (args.Length == 0)
            {
                p.StartInfo.FileName = Path.Combine(launcherPath ,@"Python\python.exe");
                p.StartInfo.Arguments =
                    @"python -c '''
import os
sys.path.append('"+ Path.Combine(launcherPath, @"Python\Lib\site-packages") +@"')

import qpt
qpt.run.run_module('" + launcherPath + @"')
'''";
            }
            // ToDO qpt启动方式
            else
            {
                // ToDO抓环境变量然后启动解释器
                p.StartInfo.FileName = Path.Combine(launcherPath, @"Python\python.exe");
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
