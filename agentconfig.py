#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentConfig-CLI
轻量级AI Agent统一配置管理器
Lightweight AI Agent Unified Configuration Manager

Zero Dependencies, Pure Python, Cross-Platform
"""

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

__version__ = "1.0.0"
__author__ = "AgentConfig Team"

# ============ 常量定义 ============
APP_NAME = "agentconfig"
CONFIG_DIR = Path.home() / ".config" / APP_NAME
BACKUP_DIR = CONFIG_DIR / "backups"
TEMPLATES_DIR = CONFIG_DIR / "templates"
PROFILES_DIR = CONFIG_DIR / "profiles"
STATE_FILE = CONFIG_DIR / "state.json"

# 支持的Agent工具配置路径映射
AGENT_PATHS = {
    "claude-code": {
        "dir": Path.home() / ".claude",
        "files": ["settings.json", "CLAUDE.md"],
    },
    "cursor": {
        "dir": Path.home() / ".cursor",
        "files": ["settings.json", "rules.md"],
    },
    "windsurf": {
        "dir": Path.home() / ".windsurf",
        "files": ["settings.json"],
    },
    "goose": {
        "dir": Path.home() / ".config" / "goose",
        "files": ["config.yaml"],
    },
    "aider": {
        "dir": Path.home() / ".aider",
        "files": ["conf.yml"],
    },
    "continue": {
        "dir": Path.home() / ".continue",
        "files": ["config.json"],
    },
}

# 内置配置模板
BUILTIN_TEMPLATES = {
    "dev": {
        "name": "开发模式",
        "name_en": "Development Mode",
        "description": "优化代码编写、调试和重构的配置",
        "description_en": "Optimized for coding, debugging and refactoring",
        "agents": {
            "claude-code": {
                "settings.json": {
                    "temperature": 0.2,
                    "max_tokens": 4096,
                    "system_prompt": "You are an expert software engineer. Focus on clean code, best practices, and comprehensive testing. Always suggest improvements and catch potential bugs."
                },
                "CLAUDE.md": "# Development Mode\n\n- Focus on clean, maintainable code\n- Suggest unit tests for new functions\n- Use type hints and docstrings\n- Prefer explicit over implicit"
            },
            "cursor": {
                "settings.json": {
                    "aiRules": [
                        "Write clean, self-documenting code",
                        "Add comprehensive error handling",
                        "Follow language-specific style guides",
                        "Suggest tests for all new features"
                    ]
                }
            }
        }
    },
    "writing": {
        "name": "写作模式",
        "name_en": "Writing Mode",
        "description": "优化文档撰写、内容创作和编辑的配置",
        "description_en": "Optimized for documentation and content creation",
        "agents": {
            "claude-code": {
                "settings.json": {
                    "temperature": 0.7,
                    "max_tokens": 8192,
                    "system_prompt": "You are a technical writer and editor. Help create clear, engaging, and well-structured documentation. Focus on readability and audience-appropriate language."
                },
                "CLAUDE.md": "# Writing Mode\n\n- Use clear, concise language\n- Structure content with proper headings\n- Include examples where helpful\n- Maintain consistent tone and style"
            }
        }
    },
    "research": {
        "name": "研究模式",
        "name_en": "Research Mode",
        "description": "优化信息检索、分析和深度研究的配置",
        "description_en": "Optimized for information retrieval and deep research",
        "agents": {
            "claude-code": {
                "settings.json": {
                    "temperature": 0.5,
                    "max_tokens": 8192,
                    "system_prompt": "You are a research assistant. Help gather, analyze, and synthesize information. Always cite sources, consider multiple perspectives, and identify gaps in knowledge."
                },
                "CLAUDE.md": "# Research Mode\n\n- Cite sources for all factual claims\n- Consider multiple viewpoints\n- Identify knowledge gaps\n- Suggest follow-up questions"
            }
        }
    },
    "minimal": {
        "name": "极简模式",
        "name_en": "Minimal Mode",
        "description": "最小化配置，让Agent保持默认行为",
        "description_en": "Minimal configuration, let agent use defaults",
        "agents": {}
    }
}


# ============ 工具函数 ============
def ensure_dirs():
    """确保所有必要的目录存在"""
    for d in [CONFIG_DIR, BACKUP_DIR, TEMPLATES_DIR, PROFILES_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def load_state():
    """加载状态文件"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"active_profile": None, "backups": [], "version": __version__}


def save_state(state):
    """保存状态文件"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def colored(text, color="white", bold=False):
    """跨平台彩色输出（无依赖）"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "gray": "\033[90m",
    }
    reset = "\033[0m"
    bold_code = "\033[1m" if bold else ""
    if sys.platform == "win32" and not os.environ.get("TERM"):
        return text
    return f"{bold_code}{colors.get(color, '')}{text}{reset}"


def print_banner():
    """打印程序横幅"""
    banner = f"""
╔══════════════════════════════════════════╗
║     {colored('AgentConfig-CLI', 'cyan', True)} v{__version__}              ║
║  轻量级AI Agent统一配置管理器              ║
║  Lightweight AI Agent Config Manager     ║
╚══════════════════════════════════════════╝
"""
    print(banner)


def print_success(msg):
    print(f"{colored('✓', 'green', True)} {msg}")


def print_error(msg):
    print(f"{colored('✗', 'red', True)} {msg}", file=sys.stderr)


def print_info(msg):
    print(f"{colored('ℹ', 'blue', True)} {msg}")


def print_warning(msg):
    print(f"{colored('⚠', 'yellow', True)} {msg}")


def get_detected_agents():
    """检测系统中已安装的Agent工具"""
    detected = []
    for name, paths in AGENT_PATHS.items():
        if paths["dir"].exists():
            detected.append(name)
    return detected


def copy_tree(src, dst):
    """递归复制目录，处理符号链接"""
    if not src.exists():
        return
    if src.is_symlink():
        if src.is_file():
            shutil.copy2(src, dst, follow_symlinks=False)
        return
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    else:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, symlinks=False, ignore_dangling_symlinks=True)


# ============ 核心命令 ============
def cmd_detect(args):
    """检测已安装的Agent工具"""
    print_banner()
    print(colored("🔍 正在检测系统中的AI Agent工具...", "cyan", True))
    print()

    detected = get_detected_agents()
    if not detected:
        print_warning("未检测到任何已知的AI Agent工具")
        print_info("支持的Agent: " + ", ".join(AGENT_PATHS.keys()))
        return 1

    print(colored(f"检测到 {len(detected)} 个Agent工具:", "green", True))
    print()
    for name in detected:
        paths = AGENT_PATHS[name]
        print(f"  {colored('●', 'green')} {colored(name, 'white', True)}")
        print(f"    配置目录: {paths['dir']}")
        existing_files = [f for f in paths["files"] if (paths["dir"] / f).exists()]
        if existing_files:
            print(f"    配置文件: {', '.join(existing_files)}")
        print()

    print_info("提示: 使用 'agentconfig backup' 备份当前配置")
    return 0


def cmd_backup(args):
    """备份当前所有Agent配置"""
    print_banner()
    backup_name = args.name or f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    backup_path = BACKUP_DIR / backup_name

    if backup_path.exists() and not args.force:
        print_error(f"备份 '{backup_name}' 已存在，使用 --force 覆盖")
        return 1

    print(colored(f"💾 正在创建备份: {backup_name}", "cyan", True))
    print()

    detected = get_detected_agents()
    if not detected:
        print_warning("未检测到任何Agent工具，无法备份")
        return 1

    backup_path.mkdir(parents=True, exist_ok=True)
    backed_up = []

    for name in detected:
        paths = AGENT_PATHS[name]
        src_dir = paths["dir"]
        dst_dir = backup_path / name
        try:
            copy_tree(src_dir, dst_dir)
            backed_up.append(name)
            print_success(f"已备份 {colored(name, 'white', True)}")
        except Exception as e:
            print_error(f"备份 {name} 失败: {e}")

    # 保存备份元数据
    meta = {
        "created_at": datetime.now().isoformat(),
        "agents": backed_up,
        "name": backup_name,
    }
    with open(backup_path / ".meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    # 更新状态
    state = load_state()
    state["backups"] = state.get("backups", [])
    if backup_name not in state["backups"]:
        state["backups"].append(backup_name)
    save_state(state)

    print()
    print_success(f"备份完成! 共备份 {len(backed_up)} 个Agent配置")
    print_info(f"备份位置: {backup_path}")
    return 0


def cmd_restore(args):
    """恢复配置到指定备份"""
    print_banner()
    backup_name = args.name
    backup_path = BACKUP_DIR / backup_name

    if not backup_path.exists():
        print_error(f"备份 '{backup_name}' 不存在")
        available = [d.name for d in BACKUP_DIR.iterdir() if d.is_dir()]
        if available:
            print_info(f"可用备份: {', '.join(available)}")
        return 1

    print(colored(f"📂 正在恢复备份: {backup_name}", "cyan", True))
    print()

    # 先备份当前配置（安全恢复）
    if not args.no_safe:
        print_info("安全模式: 先备份当前配置...")
        safe_backup = BACKUP_DIR / f"pre-restore-{int(time.time())}"
        detected = get_detected_agents()
        for name in detected:
            paths = AGENT_PATHS[name]
            if (backup_path / name).exists():
                try:
                    copy_tree(paths["dir"], safe_backup / name)
                except Exception:
                    pass
        print_success("当前配置已安全备份")
        print()

    restored = []
    for agent_dir in backup_path.iterdir():
        if agent_dir.name.startswith("."):
            continue
        name = agent_dir.name
        if name in AGENT_PATHS:
            dst_dir = AGENT_PATHS[name]["dir"]
            try:
                dst_dir.mkdir(parents=True, exist_ok=True)
                for item in agent_dir.iterdir():
                    if item.name.startswith("."):
                        continue
                    dst = dst_dir / item.name
                    copy_tree(item, dst)
                restored.append(name)
                print_success(f"已恢复 {colored(name, 'white', True)}")
            except Exception as e:
                print_error(f"恢复 {name} 失败: {e}")

    print()
    print_success(f"恢复完成! 共恢复 {len(restored)} 个Agent配置")
    return 0


def cmd_list(args):
    """列出所有备份和模板"""
    print_banner()
    state = load_state()

    # 列出备份
    print(colored("📦 配置备份列表", "cyan", True))
    print("-" * 50)
    backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir()], key=lambda x: x.stat().st_mtime, reverse=True)
    if not backups:
        print_warning("暂无备份")
    else:
        for b in backups:
            meta_file = b / ".meta.json"
            meta = {}
            if meta_file.exists():
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            agents = meta.get("agents", [])
            created = meta.get("created_at", "未知")
            if isinstance(created, str) and "T" in created:
                created = created.replace("T", " ").split(".")[0]
            print(f"  {colored('●', 'green')} {colored(b.name, 'white', True)}")
            print(f"    时间: {created} | Agent: {', '.join(agents) if agents else 'N/A'}")
    print()

    # 列出模板
    print(colored("📋 配置模板列表", "cyan", True))
    print("-" * 50)
    for key, template in BUILTIN_TEMPLATES.items():
        active = ""
        if state.get("active_profile") == key:
            active = colored(" [当前激活]", "green", True)
        print(f"  {colored('◆', 'magenta')} {colored(key, 'white', True)}{active}")
        print(f"    {template['name']} | {template['description']}")
    print()

    # 列出已检测Agent
    print(colored("🤖 已安装Agent工具", "cyan", True))
    print("-" * 50)
    detected = get_detected_agents()
    if detected:
        for name in detected:
            print(f"  {colored('✓', 'green')} {name}")
    else:
        print_warning("未检测到任何Agent工具")
    print()

    return 0


def cmd_switch(args):
    """切换到指定配置模板"""
    print_banner()
    template_name = args.template

    if template_name not in BUILTIN_TEMPLATES:
        print_error(f"未知模板: {template_name}")
        print_info(f"可用模板: {', '.join(BUILTIN_TEMPLATES.keys())}")
        return 1

    template = BUILTIN_TEMPLATES[template_name]
    print(colored(f"🔄 正在切换到模板: {template['name']} ({template_name})", "cyan", True))
    print(f"   {template['description']}")
    print()

    # 先备份当前配置
    print_info("自动备份当前配置...")
    auto_backup = f"auto-{int(time.time())}"
    auto_backup_path = BACKUP_DIR / auto_backup
    detected = get_detected_agents()
    auto_backup_path.mkdir(parents=True, exist_ok=True)
    for name in detected:
        paths = AGENT_PATHS[name]
        try:
            copy_tree(paths["dir"], auto_backup_path / name)
        except Exception:
            pass
    print_success("自动备份完成")
    print()

    # 应用模板配置
    applied = []
    for agent_name, files in template.get("agents", {}).items():
        if agent_name not in AGENT_PATHS:
            continue
        agent_dir = AGENT_PATHS[agent_name]["dir"]
        agent_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            filepath = agent_dir / filename
            try:
                if isinstance(content, dict):
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(content, f, indent=2, ensure_ascii=False)
                else:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                applied.append(f"{agent_name}/{filename}")
                print_success(f"已应用 {agent_name}/{filename}")
            except Exception as e:
                print_error(f"应用 {agent_name}/{filename} 失败: {e}")

    # 更新状态
    state = load_state()
    state["active_profile"] = template_name
    save_state(state)

    print()
    print_success(f"切换完成! 共应用 {len(applied)} 个配置文件")
    print_info(f"当前配置: {colored(template['name'], 'cyan', True)}")
    print_info(f"自动备份: {auto_backup}")
    return 0


def cmd_export(args):
    """导出配置到指定路径"""
    print_banner()
    export_path = Path(args.path).expanduser().resolve()

    print(colored(f"📤 正在导出配置到: {export_path}", "cyan", True))
    print()

    detected = get_detected_agents()
    if not detected:
        print_warning("未检测到任何Agent工具")
        return 1

    export_path.mkdir(parents=True, exist_ok=True)
    exported = []

    for name in detected:
        paths = AGENT_PATHS[name]
        try:
            copy_tree(paths["dir"], export_path / name)
            exported.append(name)
            print_success(f"已导出 {colored(name, 'white', True)}")
        except Exception as e:
            print_error(f"导出 {name} 失败: {e}")

    # 导出元数据
    meta = {
        "exported_at": datetime.now().isoformat(),
        "agents": exported,
        "version": __version__,
    }
    with open(export_path / ".agentconfig-export.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print()
    print_success(f"导出完成! 共导出 {len(exported)} 个Agent配置")
    return 0


def cmd_import(args):
    """从指定路径导入配置"""
    print_banner()
    import_path = Path(args.path).expanduser().resolve()

    if not import_path.exists():
        print_error(f"导入路径不存在: {import_path}")
        return 1

    print(colored(f"📥 正在从 {import_path} 导入配置", "cyan", True))
    print()

    imported = []
    for agent_dir in import_path.iterdir():
        if agent_dir.name.startswith("."):
            continue
        name = agent_dir.name
        if name in AGENT_PATHS:
            dst_dir = AGENT_PATHS[name]["dir"]
            try:
                dst_dir.mkdir(parents=True, exist_ok=True)
                for item in agent_dir.iterdir():
                    if item.name.startswith("."):
                        continue
                    dst = dst_dir / item.name
                    copy_tree(item, dst)
                imported.append(name)
                print_success(f"已导入 {colored(name, 'white', True)}")
            except Exception as e:
                print_error(f"导入 {name} 失败: {e}")

    print()
    print_success(f"导入完成! 共导入 {len(imported)} 个Agent配置")
    return 0


def cmd_clean(args):
    """清理旧备份"""
    print_banner()
    state = load_state()
    backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir()], key=lambda x: x.stat().st_mtime)

    keep = args.keep or 10
    if len(backups) <= keep:
        print_info(f"当前只有 {len(backups)} 个备份，无需清理 (保留阈值: {keep})")
        return 0

    to_remove = backups[:-keep]
    print(colored(f"🧹 正在清理 {len(to_remove)} 个旧备份 (保留最近 {keep} 个)", "yellow", True))
    print()

    for b in to_remove:
        try:
            shutil.rmtree(b)
            print_success(f"已删除 {b.name}")
        except Exception as e:
            print_error(f"删除 {b.name} 失败: {e}")

    print()
    print_success("清理完成")
    return 0


def cmd_version(args):
    """显示版本信息"""
    print_banner()
    print(f"版本: {colored(__version__, 'cyan', True)}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"平台: {sys.platform}")
    print(f"配置目录: {CONFIG_DIR}")
    return 0


# ============ 主程序 ============
def main():
    ensure_dirs()

    parser = argparse.ArgumentParser(
        prog="agentconfig",
        description="AgentConfig-CLI - 轻量级AI Agent统一配置管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  agentconfig detect              检测已安装的Agent工具
  agentconfig backup              备份当前配置
  agentconfig backup --name mybak 指定名称备份
  agentconfig restore --name mybak 恢复指定备份
  agentconfig switch dev          切换到开发模式
  agentconfig list                列出备份和模板
  agentconfig export ./my-config  导出配置
  agentconfig import ./my-config  导入配置
  agentconfig clean --keep 5      只保留最近5个备份
        """
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # detect
    p_detect = subparsers.add_parser("detect", help="检测已安装的AI Agent工具")
    p_detect.set_defaults(func=cmd_detect)

    # backup
    p_backup = subparsers.add_parser("backup", help="备份当前Agent配置")
    p_backup.add_argument("--name", "-n", help="备份名称")
    p_backup.add_argument("--force", "-f", action="store_true", help="强制覆盖")
    p_backup.set_defaults(func=cmd_backup)

    # restore
    p_restore = subparsers.add_parser("restore", help="恢复Agent配置")
    p_restore.add_argument("--name", "-n", required=True, help="备份名称")
    p_restore.add_argument("--no-safe", action="store_true", help="跳过安全备份")
    p_restore.set_defaults(func=cmd_restore)

    # list
    p_list = subparsers.add_parser("list", help="列出备份、模板和已安装Agent")
    p_list.set_defaults(func=cmd_list)

    # switch
    p_switch = subparsers.add_parser("switch", help="切换到指定配置模板")
    p_switch.add_argument("template", help="模板名称 (dev/writing/research/minimal)")
    p_switch.set_defaults(func=cmd_switch)

    # export
    p_export = subparsers.add_parser("export", help="导出配置到指定路径")
    p_export.add_argument("path", help="导出路径")
    p_export.set_defaults(func=cmd_export)

    # import
    p_import = subparsers.add_parser("import", help="从指定路径导入配置")
    p_import.add_argument("path", help="导入路径")
    p_import.set_defaults(func=cmd_import)

    # clean
    p_clean = subparsers.add_parser("clean", help="清理旧备份")
    p_clean.add_argument("--keep", "-k", type=int, help="保留数量 (默认10)")
    p_clean.set_defaults(func=cmd_clean)

    # version
    p_version = subparsers.add_parser("version", help="显示版本信息")
    p_version.set_defaults(func=cmd_version)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
