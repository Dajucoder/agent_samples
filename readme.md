# My Agents Project

这是一个用于构建和管理各种 AI 代理的开源项目，使用 Google Generative AI SDK 构建。

## 项目结构

- `agents/`: 包含具体代理实现的目录。
- `main.py`: 运行示例代理的入口点。
- `requirements.txt`: 项目依赖列表。

## 快速开始

1.  **安装依赖**:
    确保你已经激活了虚拟环境。
    ```bash
    pip install -r requirements.txt
    ```

2.  **配置环境变量**:
    在项目根目录创建一个 `.env` 文件，并添加你的 Google API Key：
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

3.  **运行示例代理**:
    ```bash
    python main.py
    ```

## 示例代理: WeatherAgent

本项目包含一个 `WeatherAgent` 作为示例。它演示了：
-   使用 `google-generativeai` 库。
-   定义和使用工具（函数调用）。
-   与 Gemini 模型进行对话。

## 创建新代理

1.  在 `agents/` 中创建一个新目录。
2.  创建一个类，初始化 `google.generativeai` 模型。
3.  定义工具函数并传递给模型。
4.  实现 `run` 方法来处理用户输入。

## 许可证

MIT License
