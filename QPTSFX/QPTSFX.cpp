#include <windows.h>
#include<iostream>
using namespace std;

// 无窗口模式
#pragma comment(linker, "/subsystem:\"windows\" /entry:\"mainCRTStartup\"" )

int main(int argc, char** argv) {
	std::string shell = "cmd /c configs\\entry.cmd ";
	if (argc > 1) {
		std::string subShell = "";
		subShell += '^"';
		for (int i = 1; i < argc; i++) {
			subShell += " " + string(argv[i]);
		}
		subShell += '^"';
		shell += subShell;
	}

	WinExec(shell.c_str(), SW_HIDE);
	return 0;
}
