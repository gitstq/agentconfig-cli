#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentConfig-CLI Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentconfig-cli",
    version="1.0.0",
    author="AgentConfig Team",
    author_email="agentconfig@example.com",
    description="轻量级AI Agent统一配置管理器 | Lightweight AI Agent Unified Configuration Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/agentconfig-cli",
    py_modules=["agentconfig"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "agentconfig=agentconfig:main",
        ],
    },
    keywords="ai agent configuration cli tool developer productivity",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/agentconfig-cli/issues",
        "Source": "https://github.com/gitstq/agentconfig-cli",
    },
)
