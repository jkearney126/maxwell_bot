#!/usr/bin/env python3
"""MCP Server for magnetics physics calculations."""

import sys
import json
from mcp.server import Server
from mcp.types import Tool, TextContent

# Import tool modules
from tools import fields, circuits, materials, converters

app = Server("magnetics-sme")


# Tool definitions
def get_tools() -> list[Tool]:
    """Define all available tools for the MCP server."""
    return [
        Tool(
            name="solenoid_field",
            description="Compute magnetic field at the center of a solenoid using B = μ₀ · n · I",
            inputSchema={
                "type": "object",
                "properties": {
                    "turns": {
                        "type": "integer",
                        "description": "Number of turns in the solenoid"
                    },
                    "length_m": {
                        "type": "number",
                        "description": "Length of the solenoid in meters"
                    },
                    "current_A": {
                        "type": "number",
                        "description": "Current through the solenoid in amperes"
                    }
                },
                "required": ["turns", "length_m", "current_A"]
            }
        ),
        Tool(
            name="biot_savart_wire",
            description="Compute magnetic field at distance r from an infinite straight wire using B = μ₀I / (2πr)",
            inputSchema={
                "type": "object",
                "properties": {
                    "current_A": {
                        "type": "number",
                        "description": "Current in the wire in amperes"
                    },
                    "distance_m": {
                        "type": "number",
                        "description": "Perpendicular distance from the wire in meters"
                    }
                },
                "required": ["current_A", "distance_m"]
            }
        ),
        Tool(
            name="magnetic_flux",
            description="Compute magnetic flux through a surface using Φ = B · A · cos(θ)",
            inputSchema={
                "type": "object",
                "properties": {
                    "B_tesla": {
                        "type": "number",
                        "description": "Magnetic flux density in Tesla"
                    },
                    "area_m2": {
                        "type": "number",
                        "description": "Area of the surface in square meters"
                    },
                    "angle_deg": {
                        "type": "number",
                        "description": "Angle between B and normal to surface in degrees (default 0)",
                        "default": 0
                    }
                },
                "required": ["B_tesla", "area_m2"]
            }
        ),
        Tool(
            name="reluctance",
            description="Compute reluctance of a magnetic circuit path using R = l / (μ₀ · μr · A)",
            inputSchema={
                "type": "object",
                "properties": {
                    "length_m": {
                        "type": "number",
                        "description": "Length of the magnetic path in meters"
                    },
                    "area_m2": {
                        "type": "number",
                        "description": "Cross-sectional area in square meters"
                    },
                    "relative_permeability": {
                        "type": "number",
                        "description": "Relative permeability of the material (dimensionless)"
                    }
                },
                "required": ["length_m", "area_m2", "relative_permeability"]
            }
        ),
        Tool(
            name="mmf_required",
            description="Compute magnetomotive force (MMF) needed using MMF = H · l",
            inputSchema={
                "type": "object",
                "properties": {
                    "H_field": {
                        "type": "number",
                        "description": "Magnetic field strength in A/m"
                    },
                    "path_length_m": {
                        "type": "number",
                        "description": "Length of the magnetic path in meters"
                    }
                },
                "required": ["H_field", "path_length_m"]
            }
        ),
        Tool(
            name="energy_stored",
            description="Compute energy stored in a magnetic field using W = (B² / (2μ₀)) · Volume",
            inputSchema={
                "type": "object",
                "properties": {
                    "B_tesla": {
                        "type": "number",
                        "description": "Magnetic flux density in Tesla"
                    },
                    "volume_m3": {
                        "type": "number",
                        "description": "Volume of the field in cubic meters"
                    }
                },
                "required": ["B_tesla", "volume_m3"]
            }
        ),
        Tool(
            name="material_lookup",
            description="Return properties of a named magnetic material (iron, silicon_steel, ferrite, neodymium, mu_metal, air)",
            inputSchema={
                "type": "object",
                "properties": {
                    "material": {
                        "type": "string",
                        "description": "Name of the material (e.g., 'iron', 'silicon_steel', 'ferrite', 'neodymium')"
                    }
                },
                "required": ["material"]
            }
        ),
        Tool(
            name="unit_convert",
            description="Convert between magnetic units (T↔Gauss, Wb↔Maxwell, A/m↔Oersted, H↔mH↔uH)",
            inputSchema={
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "The numerical value to convert"
                    },
                    "from_unit": {
                        "type": "string",
                        "description": "The unit to convert from (e.g., 'T', 'Gauss', 'Wb', 'Maxwell', 'A/m', 'Oersted', 'H', 'mH', 'uH')"
                    },
                    "to_unit": {
                        "type": "string",
                        "description": "The unit to convert to"
                    }
                },
                "required": ["value", "from_unit", "to_unit"]
            }
        ),
    ]


@app.list_tools()
async def list_tools():
    """List all available tools."""
    return get_tools()


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool and return the result."""
    try:
        if name == "solenoid_field":
            result = fields.solenoid_field(
                turns=arguments["turns"],
                length_m=arguments["length_m"],
                current_A=arguments["current_A"]
            )
        elif name == "biot_savart_wire":
            result = fields.biot_savart_wire(
                current_A=arguments["current_A"],
                distance_m=arguments["distance_m"]
            )
        elif name == "magnetic_flux":
            result = fields.magnetic_flux(
                B_tesla=arguments["B_tesla"],
                area_m2=arguments["area_m2"],
                angle_deg=arguments.get("angle_deg", 0)
            )
        elif name == "reluctance":
            result = circuits.reluctance(
                length_m=arguments["length_m"],
                area_m2=arguments["area_m2"],
                relative_permeability=arguments["relative_permeability"]
            )
        elif name == "mmf_required":
            result = circuits.mmf_required(
                H_field=arguments["H_field"],
                path_length_m=arguments["path_length_m"]
            )
        elif name == "energy_stored":
            result = fields.energy_stored(
                B_tesla=arguments["B_tesla"],
                volume_m3=arguments["volume_m3"]
            )
        elif name == "material_lookup":
            result = materials.lookup_material(arguments["material"])
        elif name == "unit_convert":
            result = converters.convert_unit(
                value=arguments["value"],
                from_unit=arguments["from_unit"],
                to_unit=arguments["to_unit"]
            )
        else:
            result = {"error": f"Unknown tool: {name}"}

        return [TextContent(type="text", text=json.dumps(result))]

    except (TypeError, KeyError, ValueError) as e:
        error_result = {"error": f"Tool execution failed: {str(e)}"}
        return [TextContent(type="text", text=json.dumps(error_result))]


async def main():
    """Run the MCP server."""
    async with app.run():
        pass


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
