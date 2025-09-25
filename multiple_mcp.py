from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager, AsyncExitStack
from fastmcp import FastMCP

# 创建 MCP A 服务器实例
mcp_a = FastMCP("MCP A Server", stateless_http=True)

# 添加一个工具：计算加法
@mcp_a.tool()
def add_numbers(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b

# 创建 MCP B 服务器实例
mcp_b = FastMCP("MCP B Server", stateless_http=True)

# 添加一个工具：反转字符串
@mcp_b.tool()
def reverse_string(text: str) -> str:
    """反转输入字符串。"""
    return text[::-1]

# 为 mcp_a 创建 ASGI 应用
mcp_a_app = mcp_a.http_app(path='/')

# 为 mcp_b 创建 ASGI 应用
mcp_b_app = mcp_b.http_app(path='/')

# 组合多个 lifespan 的自定义 lifespan
@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    stack = AsyncExitStack()
    try:
        # 进入所有子应用的 lifespan（初始化任务组）
        await stack.enter_async_context(mcp_a_app.lifespan(app))
        await stack.enter_async_context(mcp_b_app.lifespan(app))
        yield  # 应用运行期间
    finally:
        # 退出时自动关闭所有（shutdown）
        await stack.aclose()

# 创建主 FastAPI 应用，并设置组合 lifespan
main_app = FastAPI(lifespan=combined_lifespan)

# 挂载到不同路径
main_app.mount("/mcp_a", mcp_a_app)
main_app.mount("/mcp_b", mcp_b_app)

if __name__ == "__main__":
    # 运行主应用
    uvicorn.run(main_app, host="127.0.0.1", port=8000)