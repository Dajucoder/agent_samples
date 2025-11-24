# My Agents Project

这是一个用于构建和管理各种 AI 代理的开源项目，当前示例聚焦于一个基于 Google ADK 的「Tech Scout」情报官，用来汇总全球 AI/科技资讯。

## 项目结构

- `agents/`: 包含具体代理实现的目录。
- `agents/tech_scout/`: RSS 情报官代理的实现（`agent.py`、`__init__.py`）。
- `requirements.txt`: 项目依赖列表。

## 快速开始

1.  **安装依赖**:
    确保你已经激活了虚拟环境。
    ```bash
    pip install -r requirements.txt
    ```

2.  **配置环境变量**:
    在项目根目录创建 `.env`，并配置 Tech Scout 所需的代理与模型信息：
    ```env
    IFLOW_API_BASE=https://your-openai-compatible-base
    IFLOW_API_KEY=sk-xxx
    MODELNAME=gpt-4o-mini
    # 可选：如需走本地代理
    HTTP_PROXY=http://127.0.0.1:7890
    HTTPS_PROXY=http://127.0.0.1:7890
    ```

3.  **运行示例代理**:
    ```bash
    # 方式1：使用 ADK Web 启动
    cd agents
    adk web

    # 方式2：单独调试 Tech Scout Agent
    python -m agents.tech_scout.agent
    ```

## 示例代理: Tech Scout

`Tech Scout` 是一个 RSS 驱动的全球科技情报官：
- 使用 `google-adk` + `LiteLlm` 将开源模型/兼容 OpenAI 的服务接入 ADK。
- 内置 `rss_reader_tool`，可根据关键词命中 Hugging Face、OpenAI、MIT Tech Review、Reddit 等源。
- 自动总结最近 5 条资讯、输出中文洞察以及原文链接。
- 支持通过 `.env` 或系统变量配置代理和模型，方便在本地或服务器运行。

## 创建新代理

1.  在 `agents/` 中创建一个新目录。
2.  创建一个类，初始化 `google.generativeai` 模型。
3.  定义工具函数并传递给模型。
4.  实现 `run` 方法来处理用户输入。

## 许可证

MIT License
