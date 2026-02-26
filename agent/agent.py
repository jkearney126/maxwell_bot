#!/usr/bin/env python3
"""Magnetics SME Agent using Anthropic SDK with MCP server."""

import asyncio
import json
import os
import subprocess
import sys
from typing import Optional

from anthropic import Anthropic
from mcp.client.stdio import stdio_client


class MagneticsSMEAgent:
    """Agent with expertise in magnetics/electromagnetics powered by an MCP server."""

    def __init__(self):
        """Initialize the agent with MCP server and Anthropic client."""
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-6"
        self.tools = []
        self.server_process = None
        self.mcp_session = None

    async def start_mcp_server(self) -> bool:
        """
        Start the MCP server as a subprocess and discover tools.

        Returns:
            True if server started successfully, False otherwise
        """
        try:
            # Start the MCP server subprocess
            self.server_process = await asyncio.create_subprocess_exec(
                sys.executable,
                "mcp_server/server.py",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            # Connect to the server via stdio
            self.mcp_session = stdio_client(
                self.server_process.stdout,
                self.server_process.stdin
            )

            async with self.mcp_session as session:
                # Get tools from MCP server
                tools_response = await session.list_tools()
                self.tools = self._convert_mcp_tools_to_anthropic(tools_response.tools)

            return True

        except Exception as e:
            print(f"Error starting MCP server: {e}")
            return False

    def _convert_mcp_tools_to_anthropic(self, mcp_tools) -> list:
        """
        Convert MCP tool schemas to Anthropic format.

        Args:
            mcp_tools: Tools from MCP server

        Returns:
            List of tools in Anthropic format
        """
        anthropic_tools = []
        for tool in mcp_tools:
            anthropic_tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            })
        return anthropic_tools

    async def call_tool(self, tool_name: str, tool_input: dict) -> str:
        """
        Execute a tool via the MCP server.

        Args:
            tool_name: Name of the tool to call
            tool_input: Input parameters for the tool

        Returns:
            Tool result as a string
        """
        try:
            async with self.mcp_session as session:
                result = await session.call_tool(tool_name, tool_input)
                # Extract text content from result
                if result.content and len(result.content) > 0:
                    return result.content[0].text
                return json.dumps({"error": "Empty result from tool"})
        except Exception as e:
            return json.dumps({"error": f"Tool execution failed: {str(e)}"})

    def get_system_prompt(self) -> str:
        """Return the system prompt for the SME agent."""
        return """You are a Senior Magnetics Engineer and physicist with deep expertise in:
- Maxwell's equations and their physical interpretations
- Static and dynamic magnetic field analysis
- Magnetic circuit design (reluctance, MMF, flux)
- Soft and hard magnetic materials
- Inductors, transformers, and electromagnet design
- SI and CGS unit systems for magnetics

When solving problems:
1. Identify the relevant physical principle or equation
2. Use the available tools to perform calculations precisely
3. Show your reasoning — explain what equation applies and why
4. Call out any assumptions (e.g. uniform field, linear material)
5. Always include units in your final answer

You have access to a set of magnetics calculation tools. Use them whenever
numerical computation is required rather than estimating by hand."""

    async def run_agentic_loop(self, user_message: str) -> None:
        """
        Run the main agentic loop.

        Args:
            user_message: The initial user query
        """
        messages = [{"role": "user", "content": user_message}]

        print(f"\n{'='*70}")
        print(f"User: {user_message}")
        print(f"{'='*70}\n")

        while True:
            # Call Claude with tools
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.get_system_prompt(),
                tools=self.tools,
                messages=messages,
            )

            # Check stop reason
            if response.stop_reason == "end_turn":
                # Extract final text response
                for block in response.content:
                    if hasattr(block, "text"):
                        print(f"Agent: {block.text}\n")
                break

            elif response.stop_reason == "tool_use":
                # Process tool calls
                tool_results = []
                for block in response.content:
                    if hasattr(block, "text"):
                        # Print any text content
                        if block.text.strip():
                            print(f"Agent: {block.text}\n")

                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        tool_use_id = block.id

                        print(f"🔧 Calling tool: {tool_name}")
                        print(f"   Input: {json.dumps(tool_input, indent=2)}")

                        # Execute tool
                        result = await self.call_tool(tool_name, tool_input)
                        result_obj = json.loads(result)

                        print(f"   Result: {json.dumps(result_obj, indent=2)}\n")

                        # Collect tool result
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": result,
                        })

                # Add assistant response and tool results to messages
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

            else:
                print(f"Unexpected stop reason: {response.stop_reason}")
                break

    async def cleanup(self) -> None:
        """Clean up resources."""
        if self.server_process:
            self.server_process.terminate()
            try:
                await asyncio.wait_for(self.server_process.wait(), timeout=5)
            except asyncio.TimeoutError:
                self.server_process.kill()


async def main():
    """Main entry point."""
    agent = MagneticsSMEAgent()

    # Start MCP server
    print("Starting MCP server...")
    if not await agent.start_mcp_server():
        print("Failed to start MCP server")
        sys.exit(1)

    print(f"✓ MCP server started with {len(agent.tools)} tools\n")

    # Example questions
    test_queries = [
        "What is the magnetic field at the center of a solenoid with 500 turns, 20cm long, carrying 2A?",
        "I'm designing a magnetic circuit with a 10cm iron core (μr=5000), 2cm² cross-section. What is the reluctance?",
        "How much energy is stored in a 50mT field occupying 0.5 liters?",
    ]

    try:
        for query in test_queries:
            await agent.run_agentic_loop(query)
            print("\n")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
