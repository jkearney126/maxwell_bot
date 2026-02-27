#!/usr/bin/env python3
"""Quick test of agent startup."""

import asyncio
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from agent.agent import MagneticsSMEAgent


async def test():
    """Test agent initialization."""
    agent = MagneticsSMEAgent()

    print("Starting MCP server...")
    success = await agent.start_mcp_server()

    if success:
        print(f"✓ Server started with {len(agent.tools)} tools")
        print("\nAvailable tools:")
        for tool in agent.tools:
            print(f"  - {tool['name']}: {tool['description'][:60]}...")
    else:
        print("✗ Failed to start server")
        return 1

    # Clean up
    await agent.cleanup()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(test()))
