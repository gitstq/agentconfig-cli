<div align="center">

# 🤖 AgentConfig-CLI

**轻量级AI Agent统一配置管理器**

**Lightweight AI Agent Unified Configuration Manager**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey)]()
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)]()

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

AgentConfig-CLI 是一款**零依赖、纯Python**的轻量级命令行工具，专为解决多AI Agent开发者的配置管理痛点而生。

随着 Claude Code、Cursor、Windsurf、Goose、Aider 等AI编程工具爆发式增长，开发者的配置散落在 `~/.claude/`、`~/.cursor/`、`~/.windsurf/` 等不同目录中，团队协作时配置同步困难，新机器初始化繁琐。**AgentConfig-CLI** 让你一键备份、切换、同步所有Agent配置，像管理dotfiles一样管理AI工具配置！

**灵感来源**：GitHub Trending 上的 `cc-switch` (90k+ stars) 项目虽然功能强大但过于复杂，AgentConfig-CLI 追求**极简、零依赖、开箱即用**的极致体验。

**自研差异化亮点**：
- 🚀 **零第三方依赖** - 纯Python标准库实现，pip都不需要
- 🎯 **多Agent统一** - 支持6种主流AI Agent工具，而非仅管理编码工具
- 🔄 **场景化模板** - 内置开发/写作/研究/极简4种一键切换模板
- 💾 **安全恢复** - 每次切换自动备份，误操作可秒级回滚
- 📦 **跨平台** - Windows/macOS/Linux 全兼容

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **自动检测** | 智能扫描系统中已安装的AI Agent工具 |
| 💾 **一键备份** | 将所有Agent配置打包备份，支持自定义命名 |
| 📂 **安全恢复** | 恢复前自动备份当前配置，防止数据丢失 |
| 🔄 **模板切换** | 内置4种场景模板，一键切换不同工作模式 |
| 📤 **导入导出** | 支持配置跨机器迁移，便于团队协作 |
| 🧹 **自动清理** | 智能清理旧备份，保留最近N个版本 |
| 🎨 **彩色终端** | 美观的终端输出，支持跨平台颜色显示 |
| 🌍 **多语言** | 简体中文、繁体中文、English 完整文档 |

**支持的Agent工具**：
- ✅ Claude Code (`~/.claude`)
- ✅ Cursor (`~/.cursor`)
- ✅ Windsurf (`~/.windsurf`)
- ✅ Goose (`~/.config/goose`)
- ✅ Aider (`~/.aider`)
- ✅ Continue (`~/.continue`)

### 🚀 快速开始

#### 环境要求

- **Python** >= 3.8
- **操作系统**: Windows / macOS / Linux
- **权限**: 对用户主目录的读写权限

#### 安装步骤

**方式一：直接下载使用（推荐）**

```bash
# 克隆仓库
git clone https://github.com/gitstq/agentconfig-cli.git

# 进入目录
cd agentconfig-cli

# 直接运行（无需安装任何依赖！）
python3 agentconfig.py --help
```

**方式二：通过 pip 安装**

```bash
pip install agentconfig-cli
```

**方式三：全局安装**

```bash
# 安装到系统PATH
pip install -e .

# 现在可以直接使用
agentconfig --help
```

#### 一键运行命令

```bash
# 检测已安装的Agent工具
python3 agentconfig.py detect

# 备份当前配置
python3 agentconfig.py backup --name my-backup

# 切换到开发模式
python3 agentconfig.py switch dev

# 查看所有备份和模板
python3 agentconfig.py list

# 导出配置到指定目录
python3 agentconfig.py export ./my-agent-configs

# 从指定目录导入配置
python3 agentconfig.py import ./my-agent-configs

# 清理旧备份，只保留最近5个
python3 agentconfig.py clean --keep 5
```

### 📖 详细使用指南

#### 配置模板说明

| 模板 | 适用场景 | 核心配置 |
|------|---------|---------|
| **dev** | 代码开发 | 低temperature、注重代码质量、建议单元测试 |
| **writing** | 文档写作 | 高temperature、注重可读性、结构化输出 |
| **research** | 信息研究 | 平衡temperature、要求引用来源、多角度分析 |
| **minimal** | 默认行为 | 不修改任何配置，保持Agent原始设置 |

#### 典型使用场景

**场景1：新机器初始化**
```bash
# 在老机器上导出配置
agentconfig export ./agent-configs

# 将 ./agent-configs 复制到新机器
# 在新机器上导入
agentconfig import ./agent-configs
```

**场景2：团队协作同步**
```bash
# 导出标准团队配置
agentconfig export ./team-configs

# 提交到团队Git仓库
git add ./team-configs && git commit -m "更新Agent配置"

# 团队成员拉取后导入
agentconfig import ./team-configs
```

**场景3：工作模式切换**
```bash
# 上午写代码
agentconfig switch dev

# 下午写文档
agentconfig switch writing

# 晚上做研究
agentconfig switch research
```

### 💡 设计思路与迭代规划

**技术选型原因**：
- **纯Python标准库**：确保零依赖，任何有Python的环境都能直接运行
- **argparse**：内置模块，无需click/typer等第三方库
- **pathlib**：跨平台路径处理，替代os.path
- **json + shutil**：配置存储和文件操作的标准方案

**后续迭代计划**：
- [ ] Web UI 配置编辑器
- [ ] 自定义模板创建与管理
- [ ] 配置差异对比 (diff)
- [ ] Git 集成自动同步
- [ ] 配置加密存储
- [ ] 更多Agent工具支持 (Cline, Klein, etc.)

**社区贡献方向**：
- 提交新的Agent工具支持
- 分享你的配置模板
- 改进多语言文档
- 报告Bug和功能建议

### 📦 打包与部署指南

**本地开发**
```bash
# 克隆仓库
git clone https://github.com/gitstq/agentconfig-cli.git
cd agentconfig-cli

# 直接运行测试
python3 agentconfig.py detect
```

**打包发布**
```bash
# 构建分发包
python3 setup.py sdist bdist_wheel

# 上传到PyPI
twine upload dist/*
```

**单文件分发**
```bash
# 整个工具只有一个 agentconfig.py 文件
# 可直接复制到任何位置使用
cp agentconfig.py /usr/local/bin/agentconfig
chmod +x /usr/local/bin/agentconfig
```

### 🤝 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

**提交规范**：
- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 項目介紹

AgentConfig-CLI 是一款**零依賴、純Python**的輕量級命令列工具，專為解決多AI Agent開發者的配置管理痛點而生。

隨著 Claude Code、Cursor、Windsurf、Goose、Aider 等AI編程工具爆發式增長，開發者的配置散落在 `~/.claude/`、`~/.cursor/`、`~/.windsurf/` 等不同目錄中，團隊協作時配置同步困難，新機器初始化繁瑣。**AgentConfig-CLI** 讓你一鍵備份、切換、同步所有Agent配置，像管理dotfiles一樣管理AI工具配置！

**自研差異化亮點**：
- 🚀 **零第三方依賴** - 純Python標準庫實現
- 🎯 **多Agent統一** - 支援6種主流AI Agent工具
- 🔄 **場景化模板** - 內建開發/寫作/研究/極簡4種一鍵切換模板
- 💾 **安全恢復** - 每次切換自動備份，誤操作可秒級回滾
- 📦 **跨平台** - Windows/macOS/Linux 全相容

### ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🔍 **自動檢測** | 智能掃描系統中已安裝的AI Agent工具 |
| 💾 **一鍵備份** | 將所有Agent配置打包備份 |
| 📂 **安全恢復** | 恢復前自動備份當前配置 |
| 🔄 **模板切換** | 內建4種場景模板 |
| 📤 **匯入匯出** | 支援配置跨機器遷移 |
| 🧹 **自動清理** | 智能清理舊備份 |

### 🚀 快速開始

#### 環境要求

- **Python** >= 3.8
- **作業系統**: Windows / macOS / Linux

#### 安裝步驟

```bash
# 克隆倉庫
git clone https://github.com/gitstq/agentconfig-cli.git
cd agentconfig-cli

# 直接運行（無需安裝任何依賴！）
python3 agentconfig.py --help
```

#### 一鍵運行命令

```bash
# 檢測已安裝的Agent工具
python3 agentconfig.py detect

# 備份當前配置
python3 agentconfig.py backup --name my-backup

# 切換到開發模式
python3 agentconfig.py switch dev

# 查看所有備份和模板
python3 agentconfig.py list
```

### 📖 詳細使用指南

#### 配置模板說明

| 模板 | 適用場景 |
|------|---------|
| **dev** | 程式碼開發 |
| **writing** | 文件寫作 |
| **research** | 資訊研究 |
| **minimal** | 預設行為 |

### 💡 設計思路與迭代規劃

**技術選型原因**：
- **純Python標準庫**：確保零依賴
- **argparse**：內建模組，無需第三方庫
- **pathlib**：跨平台路徑處理

**後續迭代計劃**：
- [ ] Web UI 配置編輯器
- [ ] 自定義模板創建
- [ ] 配置差異對比
- [ ] Git 集成自動同步

### 🤝 貢獻指南

1. Fork 本倉庫
2. 創建你的特性分支
3. 提交更改
4. 創建 Pull Request

### 📄 開源協議

本項目採用 [MIT License](LICENSE) 開源協議。

---

## English

### 🎉 Introduction

AgentConfig-CLI is a **zero-dependency, pure Python** lightweight CLI tool designed to solve the configuration management pain points for multi-AI Agent developers.

As AI coding tools like Claude Code, Cursor, Windsurf, Goose, and Aider explode in popularity, developer configurations are scattered across `~/.claude/`, `~/.cursor/`, `~/.windsurf/` and other directories. Team collaboration becomes difficult, and new machine setup is tedious. **AgentConfig-CLI** lets you backup, switch, and sync all Agent configurations with one command, managing AI tool configs like dotfiles!

**Differentiation Highlights**:
- 🚀 **Zero Third-Party Dependencies** - Pure Python standard library
- 🎯 **Multi-Agent Unified** - Supports 6 mainstream AI Agent tools
- 🔄 **Scenario Templates** - Built-in dev/writing/research/minimal templates
- 💾 **Safe Recovery** - Auto-backup before switching, instant rollback
- 📦 **Cross-Platform** - Windows/macOS/Linux compatible

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Auto Detect** | Smart scan for installed AI Agent tools |
| 💾 **One-Click Backup** | Package all Agent configurations |
| 📂 **Safe Restore** | Auto-backup before restore |
| 🔄 **Template Switch** | 4 built-in scenario templates |
| 📤 **Import/Export** | Cross-machine config migration |
| 🧹 **Auto Clean** | Smart old backup cleanup |

### 🚀 Quick Start

#### Requirements

- **Python** >= 3.8
- **OS**: Windows / macOS / Linux

#### Installation

```bash
# Clone repository
git clone https://github.com/gitstq/agentconfig-cli.git
cd agentconfig-cli

# Run directly (no dependencies needed!)
python3 agentconfig.py --help
```

#### Quick Commands

```bash
# Detect installed Agent tools
python3 agentconfig.py detect

# Backup current configs
python3 agentconfig.py backup --name my-backup

# Switch to development mode
python3 agentconfig.py switch dev

# List all backups and templates
python3 agentconfig.py list
```

### 📖 Usage Guide

#### Template Reference

| Template | Use Case |
|----------|----------|
| **dev** | Code development |
| **writing** | Documentation writing |
| **research** | Information research |
| **minimal** | Default behavior |

### 💡 Design & Roadmap

**Tech Choices**:
- **Pure Python stdlib**: Zero dependencies guarantee
- **argparse**: Built-in, no third-party CLI libs
- **pathlib**: Cross-platform path handling

**Roadmap**:
- [ ] Web UI config editor
- [ ] Custom template creation
- [ ] Config diff viewer
- [ ] Git auto-sync integration

### 🤝 Contributing

1. Fork this repository
2. Create your feature branch
3. Commit your changes
4. Create a Pull Request

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ by AgentConfig Team

</div>
