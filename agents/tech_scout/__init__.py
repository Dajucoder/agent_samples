# my_agent/__init__.py

from .agent import root_agent

# 这里的 'root_agent' 必须与 agent.py 里实例化的变量名一致
__all__ = ["root_agent"]
