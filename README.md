# ADB Boom
这是一个简单的Python GUI程序，用于将ADB（Android Debug Bridge）和fastboot工具安装到Windows系统。

## 功能

- 将`Driver`文件夹复制到`C:\Program Files (x86)`目录下
- 将`adb.exe`和`fastboot.exe`添加到系统环境变量PATH中
- 提供图形界面，显示安装进度和日志

## 系统要求

- Windows操作系统
- Python 3.12（如果运行源代码）
- 管理员权限（用于修改系统PATH）

## 安装和使用

### 运行源代码

1. 确保安装了Python 3.12
2. 运行`install.py`：
   ```
   python install.py
   ```

## 打包说明

使用PyInstaller打包：
```
pyinstaller --onefile --windowed install.py
```

## 版本

当前版本：1.0

## 相关链接

- [ADB官方文档](https://developer.android.com/studio/command-line/adb)
- [fastboot官方文档](https://developer.android.com/studio/releases/platform-tools)

## 许可证

本项目仅供学习和个人使用。
