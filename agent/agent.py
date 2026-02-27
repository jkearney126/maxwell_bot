#!/usr/bin/env python3
"""Generic Agent Framework - auto-discovers and loads skills."""

import json
import os
import sys
from itertools import cycle

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anthropic import Anthropic

# Import tools dynamically
from mcp_server.tools import fields, circuits, materials, converters


class ThinkingSpinner:
    """Simple animated spinner for showing model is thinking."""

    def __init__(self):
        """Initialize spinner."""
        self.spinner_frames = cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
        self.message = "🧠 Thinking"

    def start(self):
        """Print initial thinking message."""
        print(f"\n{self.message}...", end="", flush=True)

    def stop(self):
        """Clear the spinner line."""
        print("\r" + " " * 50 + "\r", end="", flush=True)


class SkillAgent:
    """Generic agent that auto-discovers and loads skills."""

    def __init__(self, skill_name: str = None):
        """
        Initialize agent with a specific skill or auto-discover.

        Args:
            skill_name: Name of the skill directory. If None, uses first available skill.
        """
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-6"

        # Discover available skills
        self.available_skills = self._discover_skills()

        if not self.available_skills:
            raise RuntimeError(f"No skills found in skills/ directory")

        # Use provided skill or default to first
        if skill_name is None:
            self.skill_name = self.available_skills[0]
        else:
            if skill_name not in self.available_skills:
                raise ValueError(
                    f"Skill '{skill_name}' not found. Available: {', '.join(self.available_skills)}"
                )
            self.skill_name = skill_name

        self.skill_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "skills",
            self.skill_name,
        )
        self.tools = self._setup_tools()
        self.skill_md = self._load_skill_md()

    @staticmethod
    def _discover_skills() -> list:
        """Discover all available skills in skills/ directory."""
        skills_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "skills",
        )

        if not os.path.exists(skills_dir):
            return []

        skills = []
        for item in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, item)
            # Check if it's a directory with a skill.md file
            if os.path.isdir(skill_path):
                skill_file = os.path.join(skill_path, "skill.md")
                if os.path.exists(skill_file):
                    skills.append(item)

        return sorted(skills)

    def _load_skill_md(self) -> str:
        """Load skill definition from skill.md file."""
        skill_path = os.path.join(self.skill_dir, "skill.md")
        try:
            with open(skill_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"Skill '{self.skill_name}' not found at {skill_path}"

    def _setup_tools(self) -> list:
        """Set up tool definitions. In a real system, these would be parsed from skill.md."""
        # Hardcoded for magnetics-sme for now
        # In a production system, these would be extracted from skill.md
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
        """
        Generate system prompt from skill.md.

        In production, this would parse the skill.md file to create a dynamic prompt.
        For now, it uses the skill.md as context.
        """
        base_prompt = """You are an expert agent with specialized knowledge and capabilities.

You have access to the following tools to help solve problems. Use them whenever appropriate.

Here is your skill definition:

"""
        return base_prompt + self.skill_md

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
