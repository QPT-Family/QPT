#include <windows.h>
#include <iostream>
using namespace std;

// 切记，不能是64位，不然PE不好修改了
// 无窗口模式
#pragma comment(linker, "/subsystem:\"windows\" /entry:\"mainCRTStartup\"" )

int main(int argc, char** argv) {
	// 配置UTF-8
	SetConsoleCP(CP_UTF8);
	SetConsoleOutputCP(CP_UTF8);

	string shell = "cmd /c configs\\entry.cmd";
	if (argc > 1) {
		std::string subShell = " ";
		for (int i = 1; i < argc; i++) {
			subShell += "QPT_ARGS_FLAG\"" + string(argv[i])+"\"";
		}
		shell += subShell;
	}

	WinExec(shell.c_str(), SW_HIDE);
	return 0;
}
