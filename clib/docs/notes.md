# 开发笔记

## OpenFileDialog

Win32 下面实现：打开文件，保存文件，选择文件夹这三个对话框很简单，但 SDL 下在众多系统里就难了，目前三个方案：

- ncruces/zenity：一个二进制覆盖三平台，Go 编译无依赖，但用户需额外安装；
- Tiny File Dialogs (tinyfd)：C 单文件，可直接嵌入头文件，但有 6000 行 C 代码；
- Portable File Dialogs (pfd)：C++11 单个头文件，有 1800 行代码；

其中 tinyfd 和 pfd 在 Windows 下面都是用 COM 组件，而其他平台则用：zenity / kdialog / osascript 这些工具来实现；

看起来比较靠谱的是 pfd ：https://github.com/samhocevar/portable-file-dialogs 

用起来比较方便一点，暂时不打算实现到 GameLib.h 中，如果地图编辑器之类的需要，直接 pfd 吧；

