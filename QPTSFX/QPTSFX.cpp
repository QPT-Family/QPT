#include <windows.h>
#include <iostream>
using namespace std;

// 切记，不能是64位，不然PE不好修改了
// 无窗口模式
//#pragma comment(linker, "/subsystem:\"windows\" /entry:\"mainCRTStartup\"" )

int main(int argc, char** argv) {
	struct stat buffer;
	const char *configsFile = ".\\configs\\entry.cmd";
	if (stat(configsFile, &buffer) != 0) {
		MessageBox(NULL, TEXT("QPT：configs文件夹存在文件缺失，已终止！"), TEXT("执行失败 - QPT封装工具"), MB_OK | MB_ICONSTOP);
		return 1;
	};
	// 配置UTF-8
	SetConsoleCP(CP_UTF8);
	SetConsoleOutputCP(CP_UTF8);
	
	string shell = "cmd /c configs\\entry.cmd";
	if (argc > 1) {
		std::string subShell = " ";
		for (int i = 1; i < argc; i++) {
			subShell += "QPT_ARGS_FLAG\"" + string(argv[i]) + "\"";
		}
		shell += subShell;
	}
	else {
		shell += " QPT_ARGS_FLAG"; // DOS命令是我琢磨不透的东西，这个地方还是有个符号占位吧 - 下个版本用%*
	};

	WinExec(shell.c_str(), SW_HIDE);
	return 0;
}
