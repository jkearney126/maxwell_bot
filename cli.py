#!/usr/bin/env python3
"""CLI for interacting with skill-based agents."""

import sys
from agent.agent import SkillAgent


EXAMPLE_PROMPTS = [
    "What is the magnetic field at the center of a solenoid with 500 turns, 20cm long, carrying 2A?",
    "I'm designing a magnetic circuit with a 10cm iron core (μr=5000), 2cm² cross-section. What is the reluctance?",
    "How much energy is stored in a 50mT field occupying 0.5 liters?",
    "Compare the permeability of silicon steel vs ferrite.",
    "Convert 1.2 Tesla to Gauss.",
]


def print_welcome(agent: SkillAgent):
    """Print welcome message and instructions."""
    print("=" * 70)
    print(f"SKILL AGENT - {agent.skill_name.upper()}")
    print("=" * 70)
    print("\nExample prompts you can use:")
    for i, example in enumerate(EXAMPLE_PROMPTS, 1):
        print(f"  {i}. {example}")
    print("\nOr type your own question.")
    print("Type 'quit' or 'exit' to exit.\n")


def select_skill(available_skills: list) -> str:
    """
    Let user select a skill if multiple are available.

    Args:
        available_skills: List of available skill names

    Returns:
        Selected skill name
    """
    if len(available_skills) == 1:
        return available_skills[0]

    print("=" * 70)
    print("AVAILABLE SKILLS")
    print("=" * 70)
    for i, skill in enumerate(available_skills, 1):
        print(f"  {i}. {skill}")
    print()

    while True:
        try:
            choice = input("Select a skill (number): ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_skills):
                return available_skills[choice_idx]
            else:
                print(f"Invalid choice. Please select 1-{len(available_skills)}")
        except ValueError:
            print("Please enter a number")


def handle_user_input(user_input: str, agent: SkillAgent) -> bool:
    """
    Handle user input: either select example or process as query.

    Args:
        user_input: User's input from stdin
        agent: SkillAgent instance

    Returns:
        True if should continue, False if user wants to exit
    """
    if not user_input:
        return True

    # Check for exit commands
    if user_input.lower() in ["quit", "exit", "q"]:
        print("\nGoodbye!")
        return False

    # Check if user selected an example by number
    try:
        choice = int(user_input)
        if 1 <= choice <= len(EXAMPLE_PROMPTS):
            user_input = EXAMPLE_PROMPTS[choice - 1]
            print(f"Selected: {user_input}\n")
        else:
            print(
                f"Invalid choice. Please select 1-{len(EXAMPLE_PROMPTS)} or type a question.\n"
            )
            return True
    except ValueError:
        # Not a number, treat as user's question
        pass

    # Run the agentic loop
    agent.run_agentic_loop(user_input)
    print("\n" + "-" * 70 + "\n")

    return True


def main():
    """Main entry point for the CLI."""
    try:
        # Discover available skills
        available_skills = SkillAgent._discover_skills()

        if not available_skills:
            print("❌ No skills found in skills/ directory")
            sys.exit(1)

        # Select skill if multiple available
        selected_skill = select_skill(available_skills)

        # Initialize agent with selected skill
        agent = SkillAgent(skill_name=selected_skill)

        print(f"✓ Agent initialized with skill: {selected_skill}")
        print(f"✓ Loaded {len(agent.tools)} tools\n")

        print_welcome(agent)

        while True:
            # Get user input
            user_input = input("You: ").strip()

            if not handle_user_input(user_input, agent):
                break

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
