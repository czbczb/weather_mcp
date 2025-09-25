from fastmcp import Client
import asyncio

async def test_a():
    async with Client("http://127.0.0.1:8000/mcp_a") as client:  # 使用 async with 建立连接
        return await client.call_tool("add_numbers", {"a": 1, "b": 2})

async def test_b():
    async with Client("http://127.0.0.1:8000/mcp_b") as client:  # 同上
        return await client.call_tool("reverse_string", {"text": "hello"})

async def concurrent_test():
    result_a, result_b = await asyncio.gather(test_a(), test_b())
    print("**************************** Concurrent Test Results ****************************")
    print(f"A: {result_a}") 
    print("**************************** Concurrent Test Results ****************************")
    print(f"B: {result_b}") 

if __name__ == "__main__":
    asyncio.run(concurrent_test())