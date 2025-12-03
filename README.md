# JHTE 智能平台 - 独立Python版本

基于 JHTE (Jin He's Tips Engineering) 方法的智能翻译与情感分析平台（暂未开发）。需要Ollama安装的deepseek7b。

## 🎯 特点

- ✅ **完全独立**：内置Python环境，无需安装任何依赖
- ✅ **开箱即用**：双击启动脚本即可运行
- ✅ **无环境变量**：不需要配置任何系统环境变量
- ✅ **跨平台**：支持Windows、Linux、Mac系统

## 📁 项目结构

JHTE-Platform/

├── python/                    # 内置Python环境（已安装所需库）

│   ├── python.exe            # Windows可执行文件

│   ├── Scripts/              # 脚本文件夹（包含pip等）

│   └── Lib/                  # 已安装的库

├── templates/                # 前端模板文件

│   ├── index.html            # 主页面

│   ├── css/                  # 样式表(暂未加入)

│   │   └── style.css

│   ├── js/                   # 前端脚本(暂未加入)

│   │   └── script.js

│   └── images/               # 图片资源

├── other/                    # 其他资源

├── app.py                    # 后端主程序

├── requirements.txt          # 依赖列表（备用）

├── start_windows.bat         # Windows启动脚本

├── start_linux.sh            # Linux启动脚本(暂未加入)

├── start_mac.sh              # Mac启动脚本(暂未加入)


└── README.md                 # 项目说明

## 🚀 快速开始

### Windows用户

1. 双击 `start_windows.bat` 启动应用
2. 打开浏览器访问 `http://localhost:5000`

## 📊 开发进度


| 模块     | 状态      | 完成度 | 预计完成   |
| ---------- | ----------- | -------- | ------------ |
| 核心算法 | 🔶 进行中 | 50%    | 2026-02-01 |
| Web界面  | ✅ 已完成 | 90%    | 2025-11-20 |
| 独立环境 | ✅ 已完成 | 100%   | 2025-11-20 |
| 文档     | 🔶 进行中 | 80%    | 2026-02-10 |


## 👥 作者

* **CTVHe** - 初始工作
* **Jin He** - 初始工作

## 📞 联系与支持

* **项目维护者** ：CTVHe
* **联系邮箱** ：3360760850@qq.com

## 🎯 下一步计划

* 完善翻译引擎核心算法
* 优化Web界面用户体验
* 实现API接口的情感分析算法
