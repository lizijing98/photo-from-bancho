# Agent 运行环境准备

本文件供 Agent 在安装 Skill 或执行裁切、拼接前读取。Skill 的发现和加载方式由当前 Agent 平台决定，安装时应保留整个 `photo-from-bancho` 目录。

## 1. 检查当前环境

- 图像生成需要读取参考图并支持图像生成或编辑的工具。缺少图像工具时，按 [SKILL.md](SKILL.md) 提供提示词，收到可用的模拟截图后再执行拼接。
- 裁切与拼接需要可运行本地命令的环境、可写的输出目录，以及 Python 3.9 或更高版本。先检查当前可用的解释器。macOS 和 Linux 通常使用 `python3`，Windows 可用 `py -3` 或 `python`。
- 用同一个解释器检查 Pillow 能否导入，并把版本与 [requirements.txt](requirements.txt) 对照。版本符合要求时，直接复用该解释器。当前要求为 Pillow 11.3.0 或更高版本。

```bash
python3 -c "import sys; print(sys.executable); print(sys.version.split()[0]); sys.exit(0 if sys.version_info >= (3, 9) else 1)"
python3 -c "from PIL import Image, ImageOps; print(Image.__version__)"
```

## 2. 按需安装 Pillow

只有导入失败或版本不满足要求时才安装。把下列命令中的 `SKILL_DIR` 和 `VENV_DIR` 分别替换为本 Skill 的实际目录和可写工作区内的隔离环境路径。路径带空格时保留引号。可使用临时目录，也可复用同一个 Skill 已创建的虚拟环境。

macOS 或 Linux：

```bash
python3 -m venv "VENV_DIR"
"VENV_DIR/bin/python" -m pip install -r "SKILL_DIR/requirements.txt"
"VENV_DIR/bin/python" -c "from PIL import Image, ImageOps; print(Image.__version__)"
```

Windows PowerShell：

```powershell
py -3 -m venv "VENV_DIR"
& "VENV_DIR\Scripts\python.exe" -m pip install -r "SKILL_DIR\requirements.txt"
& "VENV_DIR\Scripts\python.exe" -c "from PIL import Image, ImageOps; print(Image.__version__)"
```

安装和复查成功后，用该虚拟环境的 Python 执行 `trim_screenshot.py` 和 `compose.py`。不需要激活虚拟环境，也不需要修改全局 Python 或用户已有项目的依赖配置。

若没有合格的 Python、无法执行本地命令，或因网络和权限限制无法安装，说明具体缺项并保留已完成的产物。遵循当前平台的权限流程，不擅自安装系统组件、配置 API 密钥或切换付费服务。
