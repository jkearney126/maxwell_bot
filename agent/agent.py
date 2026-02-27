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
from agent.knowledge_base import KnowledgeBase


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
        self.skill_md = self._load_skill_md()
        self.tools = self._setup_tools()
        self.knowledge_base = KnowledgeBase(self.skill_dir)

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

    def _parse_tools_from_skill_md(self) -> list:
        """Parse tool definitions from the skill.md file."""
        tools = []
        lines = self.skill_md.split("\n")
        in_tool_section = False
        i = 0

        # Build a lookup table from Use Case Decision Table for fallback descriptions
        use_case_map = self._build_use_case_map(lines)

        while i < len(lines):
            line = lines[i]

            # Detect Tool Reference section
            if "## Tool Reference" in line:
                in_tool_section = True
                i += 1
                continue

            # Stop at next major section
            if in_tool_section and line.startswith("## ") and "Tool Reference" not in line:
                break

            # Extract tool header (### tool_name)
            if in_tool_section and line.startswith("### "):
                tool_name = line.replace("### ", "").strip()

                # Skip "---" separator and find code block
                i += 1
                while i < len(lines) and lines[i].strip() in ("", "---"):
                    i += 1

                # Extract code block
                if i < len(lines) and lines[i].strip().startswith("```"):
                    i += 1
                    code_lines = []
                    while i < len(lines) and not lines[i].strip().startswith("```"):
                        code_lines.append(lines[i])
                        i += 1

                    # Parse Input line from code block
                    code_text = "\n".join(code_lines)
                    input_schema = self._extract_input_schema(code_text)

                    # Collect description lines
                    description = self._extract_tool_description(lines, i, tool_name, use_case_map)

                    tool = {
                        "name": tool_name,
                        "description": description,
                        "input_schema": input_schema,
                    }
                    tools.append(tool)

                    # Skip to next tool
                    while i < len(lines) and not (lines[i].startswith("### ") or lines[i].startswith("## ")):
                        i += 1
                    continue

            i += 1

        if not tools:
            raise ValueError(
                f"No tools found in skill.md for '{self.skill_name}'. "
                "Ensure skill.md has a '## Tool Reference' section with tool definitions."
            )
        return tools

    def _build_use_case_map(self, lines: list) -> dict:
        """Build a mapping from tool names to descriptions from the Use Case table."""
        use_case_map = {}
        in_table = False
        for line in lines:
            if "## Use Case Decision Table" in line:
                in_table = True
            elif line.startswith("## ") and "Use Case" not in line:
                in_table = False
            elif in_table and "|" in line and "`" in line:
                # Parse table row like "| Solenoid/coil field strength | `solenoid_field` | Use when... |"
                parts = line.split("|")
                if len(parts) >= 3:
                    tool_part = parts[2].strip()
                    desc_part = parts[1].strip()
                    # Extract tool name from backticks
                    if "`" in tool_part:
                        tool_name = tool_part.strip("`").strip()
                        use_case_map[tool_name] = desc_part
        return use_case_map

    def _extract_tool_description(self, lines: list, start_idx: int, tool_name: str, use_case_map: dict) -> str:
        """Extract description for a tool from its documentation section."""
        i = start_idx + 1  # Skip closing ```

        while i < len(lines):
            curr_line = lines[i].strip()
            # Stop at next tool or section
            if curr_line.startswith("###") or curr_line.startswith("## "):
                break
            # Try various description formats
            if "**Use Case:**" in curr_line:
                return curr_line.split("**Use Case:**")[1].strip()
            elif "**Inputs:**" in curr_line or "**Input:**" in curr_line:
                sep = "**Inputs:**" if "**Inputs:**" in curr_line else "**Input:**"
                return curr_line.split(sep)[1].strip()
            # For tools with **Available Materials:** or **Supported Conversions:**,
            # use the fallback from use case table
            elif any(x in curr_line for x in ["**Available Materials:**", "**Supported Conversions:**"]):
                break
            i += 1

        # Fallback to use case table description
        return use_case_map.get(tool_name, "")

    def _extract_input_schema(self, code_text: str) -> dict:
        """Parse input schema from code block text like 'Input: { turns: int, ... }'."""
        schema = {"type": "object", "properties": {}, "required": []}

        # Find Input line
        for line in code_text.split("\n"):
            if line.startswith("Input:"):
                # Extract the {...} part
                input_str = line.split("Input:")[1].strip()
                input_str = input_str.strip("{").strip("}")

                # Parse each parameter
                for param_def in input_str.split(","):
                    param_def = param_def.strip()
                    if ":" in param_def:
                        name, type_str = param_def.split(":", 1)
                        name = name.strip()
                        type_str = type_str.strip().lower()

                        # Map type strings to JSON schema types
                        json_type = "number"
                        if "int" in type_str:
                            json_type = "integer"
                        elif "str" in type_str or "string" in type_str:
                            json_type = "string"
                        elif "float" in type_str or "number" in type_str:
                            json_type = "number"

                        schema["properties"][name] = {
                            "type": json_type,
                            "description": name.replace("_", " ")
                        }
                        # All parameters are required unless specified otherwise
                        schema["required"].append(name)

                break

        return schema

    def _setup_tools(self) -> list:
        """Set up tool definitions by parsing from skill.md."""
        return self._parse_tools_from_skill_md()

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

    def get_system_prompt(self, user_message: str = None) -> str:
        """
        Generate system prompt from skill.md with optional RAG context.

        Args:
            user_message: User's question for RAG retrieval (optional)
        """
        base_prompt = """You are an expert agent with specialized knowledge and capabilities.

You have access to the following tools to help solve problems. Use them whenever appropriate.

Here is your skill definition:

"""
        prompt = base_prompt + self.skill_md

        # Add retrieved knowledge context if user message provided
        if user_message:
            retrieved_docs = self.knowledge_base.retrieve(user_message, top_k=3)
            if retrieved_docs:
                knowledge_context = self.knowledge_base.format_context(retrieved_docs)
                prompt += knowledge_context

        return prompt

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
                system=self.get_system_prompt(user_message),
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
