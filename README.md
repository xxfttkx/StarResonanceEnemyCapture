# StarResonanceEnemyCapture

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-brightgreen.svg)](https://www.gnu.org/licenses/agpl-3.0.txt)

StarResonanceEnemyCapture 是一款专为《星痕共鸣》游戏开发的工具，通过网络数据包分析实现敌人信息的实时监控和管理。

## 🌟 核心功能

- **🔍 实时敌人数据捕获**: 通过网络抓包实时获取敌人信息。
- **📊 数据解析与同步**: 自动解析敌人数据并同步到内存中。
- **⚡ 高效日志记录**: 支持详细的日志记录，便于调试和问题排查。
- **🎯 模块化设计**: 易于扩展和维护的模块化代码结构。

## 📦 项目结构

```
StarResonanceEnemyCapture/
├── main.py                 # 主程序入口
├── enemy_manager.py        # 敌人数据管理模块
├── packet_capture.py       # 网络抓包模块
├── packet_parser.py        # 数据包解析模块
├── network_interface_util.py # 网络接口工具
├── logging_config.py       # 日志配置模块
├── monster_names.json      # 敌人名称映射表
├── star.proto              # Protobuf 定义文件
├── star_pb2.py             # Protobuf 生成的 Python 文件
├── logs/                   # 日志文件目录
└── requirements.txt        # Python 依赖
```

## 🚀 快速开始

### 环境要求

- **操作系统**: Windows 10/11 (64 位)
- **Python 版本**: 3.8+
- **依赖工具**: Npcap 或 WinPcap（推荐 Npcap）

### 安装依赖

1. 克隆项目：
   ```bash
   git clone https://github.com/xxfttkx/StarResonanceEnemyCapture.git
   cd StarResonanceEnemyCapture
   ```

2. 安装 Python 依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 运行程序

1. 启动程序：
   ```bash
   python main.py
   ```

2. 按照提示选择网络接口，程序将自动开始抓包并解析敌人数据。

## 🛠️ 开发者指南

### 模块说明

- **main.py**: 程序入口，初始化各模块并启动监控。
- **enemy_manager.py**: 管理敌人数据的同步与存储。
- **packet_capture.py**: 实现网络数据包的捕获。
- **packet_parser.py**: 解析捕获的数据包。
- **network_interface_util.py**: 提供网络接口的选择和管理功能。
- **logging_config.py**: 配置日志记录。

### 日志系统

- 日志文件存储在 logs 目录下。
- 启用调试模式：
  ```bash
  python main.py --debug
  ```

## 🙏 鸣谢

本项目关键数据抓取与分析部分基于 [StarResonanceAutoMod](https://github.com/fudiyangjin/StarResonanceAutoMod) 项目移植而来，感谢原作者对于本项目的帮助。

本项目关键数据抓取与分析部分基于 [StarResonanceDamageCounter](https://github.com/dmlgzs/StarResonanceDamageCounter) 项目移植而来，感谢原作者对于本项目的帮助。

## ⚖️ 许可证

本项目基于 [AGPL v3](https://www.gnu.org/licenses/agpl-3.0.txt) 许可证开源，欢迎贡献代码。

## ⚖️ 免责声明

本工具仅用于游戏数据分析学习目的，不得用于任何违反游戏服务条款的行为。使用者需自行承担相关风险。项目开发者不对任何使用本工具产生的后果负责。请在使用前确保遵守游戏社区的相关规定和道德标准。