#!/usr/bin/env python3
"""Magnetics SME Agent using Anthropic SDK."""

import asyncio
import json
import os
import sys
from itertools import cycle

# Add parent directory to path so we can import mcp_server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anthropic import Anthropic

# Import tools directly
from mcp_server.tools import fields, circuits, materials, converters


class ThinkingSpinner:
    """Simple animated spinner for showing model is thinking."""

    def __init__(self):
        """Initialize spinner."""
        self.spinner_frames = cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
        self.message = "🧠 Claude is thinking"

    def start(self):
        """Print initial thinking message."""
        print(f"\n{self.message}...", end="", flush=True)

    def tick(self):
        """Update spinner frame."""
        frame = next(self.spinner_frames)
        print(f"\r{frame} {self.message}...", end="", flush=True)

    def stop(self):
        """Clear the spinner line."""
        print("\r" + " " * 50 + "\r", end="", flush=True)


class MagneticsSMEAgent:
    """Agent with expertise in magnetics/electromagnetics."""

    def __init__(self):
        """Initialize the agent."""
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-6"
        self.tools = self._setup_tools()

    def _setup_tools(self) -> list:
        """Set up tool definitions for Claude."""
        return [
            {
                "name": "solenoid_field",
                "description": "Compute magnetic field at the center of a solenoid using B = μ₀ · n · I",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "turns": {"type": "integer", "description": "Number of turns"},
                        "length_m": {"type": "number", "description": "Length in meters"},
                        "current_A": {"type": "number", "description": "Current in amperes"},
                    },
                    "required": ["turns", "length_m", "current_A"],
                },
            },
            {
                "name": "biot_savart_wire",
                "description": "Compute magnetic field at distance r from an infinite straight wire using B = μ₀I / (2πr)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "current_A": {"type": "number", "description": "Current in amperes"},
                        "distance_m": {"type": "number", "description": "Distance from wire in meters"},
                    },
                    "required": ["current_A", "distance_m"],
                },
            },
            {
                "name": "magnetic_flux",
                "description": "Compute magnetic flux through a surface using Φ = B · A · cos(θ)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "B_tesla": {"type": "number", "description": "Flux density in Tesla"},
                        "area_m2": {"type": "number", "description": "Area in square meters"},
                        "angle_deg": {"type": "number", "description": "Angle in degrees (default 0)"},
                    },
                    "required": ["B_tesla", "area_m2"],
                },
            },
            {
                "name": "reluctance",
                "description": "Compute reluctance of a magnetic circuit path using R = l / (μ₀ · μr · A)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "length_m": {"type": "number", "description": "Path length in meters"},
                        "area_m2": {"type": "number", "description": "Cross-sectional area in m²"},
                        "relative_permeability": {"type": "number", "description": "Material's μᵣ"},
                    },
                    "required": ["length_m", "area_m2", "relative_permeability"],
                },
            },
            {
                "name": "mmf_required",
                "description": "Compute magnetomotive force (MMF) using MMF = H · l",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "H_field": {"type": "number", "description": "Field strength in A/m"},
                        "path_length_m": {"type": "number", "description": "Path length in meters"},
                    },
                    "required": ["H_field", "path_length_m"],
                },
            },
            {
                "name": "energy_stored",
                "description": "Compute energy stored in a magnetic field using W = (B² / (2μ₀)) · Volume",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "B_tesla": {"type": "number", "description": "Flux density in Tesla"},
                        "volume_m3": {"type": "number", "description": "Volume in m³"},
                    },
                    "required": ["B_tesla", "volume_m3"],
                },
            },
            {
                "name": "material_lookup",
                "description": "Return properties of a named magnetic material",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "material": {"type": "string", "description": "Material name (e.g., 'iron', 'ferrite')"},
                    },
                    "required": ["material"],
                },
            },
            {
                "name": "unit_convert",
                "description": "Convert between magnetic units (T↔Gauss, Wb↔Maxwell, A/m↔Oersted, H↔mH↔uH)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "value": {"type": "number", "description": "Value to convert"},
                        "from_unit": {"type": "string", "description": "Source unit"},
                        "to_unit": {"type": "string", "description": "Target unit"},
                    },
                    "required": ["value", "from_unit", "to_unit"],
                },
            },
        ]

    def call_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool and return the result."""
        try:
            if tool_name == "solenoid_field":
                result = fields.solenoid_field(**tool_input)
            elif tool_name == "biot_savart_wire":
                result = fields.biot_savart_wire(**tool_input)
            elif tool_name == "magnetic_flux":
                result = fields.magnetic_flux(**tool_input)
            elif tool_name == "reluctance":
                result = circuits.reluctance(**tool_input)
            elif tool_name == "mmf_required":
                result = circuits.mmf_required(**tool_input)
            elif tool_name == "energy_stored":
                result = fields.energy_stored(**tool_input)
            elif tool_name == "material_lookup":
                result = materials.lookup_material(**tool_input)
            elif tool_name == "unit_convert":
                result = converters.convert_unit(**tool_input)
            else:
                result = {"error": f"Unknown tool: {tool_name}"}

            return json.dumps(result)
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

    def run_agentic_loop(self, user_message: str) -> None:
        """Run the main agentic loop."""
        messages = [{"role": "user", "content": user_message}]

        print(f"\n{'='*70}")
        print(f"User: {user_message}")
        print(f"{'='*70}\n")

        while True:
            # Show spinner while thinking
            spinner = ThinkingSpinner()
            spinner.start()

            # Call Claude with tools
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.get_system_prompt(),
                tools=self.tools,
                messages=messages,
            )

            spinner.stop()

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
                        result = self.call_tool(tool_name, tool_input)
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


def main():
    """Main entry point with interactive chat."""
    agent = MagneticsSMEAgent()

    print(f"✓ Agent initialized with {len(agent.tools)} tools\n")

    # Example prompts
    examples = [
        "What is the magnetic field at the center of a solenoid with 500 turns, 20cm long, carrying 2A?",
        "I'm designing a magnetic circuit with a 10cm iron core (μr=5000), 2cm² cross-section. What is the reluctance?",
        "How much energy is stored in a 50mT field occupying 0.5 liters?",
        "Compare the permeability of silicon steel vs ferrite.",
        "Convert 1.2 Tesla to Gauss.",
    ]

    print("=" * 70)
    print("MAGNETICS SME AGENT - Interactive Chat")
    print("=" * 70)
    print("\nExample prompts you can use:")
    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")
    print("\nOr type your own question about electromagnetics and magnetics.")
    print("Type 'quit' or 'exit' to exit.\n")

    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break

            # Check if user selected an example by number
            try:
                choice = int(user_input)
                if 1 <= choice <= len(examples):
                    user_input = examples[choice - 1]
                    print(f"Selected: {user_input}\n")
                else:
                    print(f"Invalid choice. Please select 1-{len(examples)} or type a question.\n")
                    continue
            except ValueError:
                # Not a number, treat as user's question
                pass

            # Run the agentic loop
            agent.run_agentic_loop(user_input)
            print("\n" + "-" * 70 + "\n")

    except KeyboardInterrupt:
        print("\n\nGoodbye!")


if __name__ == "__main__":
    main()
