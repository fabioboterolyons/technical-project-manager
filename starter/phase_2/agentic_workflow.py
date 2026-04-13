# agentic_workflow.py

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Resolve paths relative to this script so the workflow runs from any working
# directory without needing special PYTHONPATH or cwd setup.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]  # technical_project_manager_agent/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(SCRIPT_DIR / ".env")
load_dotenv()

from starter.phase_1.workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, \
    EvaluationAgent, RoutingAgent

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
open_ai_key = os.getenv("OPENAI_API_KEY")
# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
PRODUCT_SPEC_PATH = SCRIPT_DIR / "Product-Spec-Email-Router.txt"
with open(PRODUCT_SPEC_PATH, "r") as f:
    product_spec = f.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(open_ai_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
    f"{product_spec}"
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(open_ai_key, persona_product_manager, knowledge_product_manager)
# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents"
product_manager_eval_criteria = (
    "The answer should be stories that follow the following structure: "
    "As a [type of user], I want [an action or feature] so that [benefit/value]."
)
product_manager_evaluation_agent = EvaluationAgent(open_ai_key, persona_product_manager_eval, product_manager_eval_criteria, product_manager_knowledge_agent, 5)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(open_ai_key, persona_program_manager, knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
program_evaluation_criteria = "The answer should be product features that follow the following structure: " \
                             "Feature Name: A clear, concise title that identifies the capability\n" \
                             "Description: A brief explanation of what the feature does and its purpose\n" \
                             "Key Functionality: The specific capabilities or actions the feature provides\n" \
                             "User Benefit: How this feature creates value for the user"
program_manager_evaluation_agent = EvaluationAgent(open_ai_key, persona_program_manager_eval, program_evaluation_criteria, program_manager_knowledge_agent, 5)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(open_ai_key, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
person_dev_engineer_eval_criteria = "The answer should be tasks following this exact structure: " \
    "Task ID: A unique identifier for tracking purposes\n" \
    "Task Title: Brief description of the specific development work\n" \
    "Related User Story: Reference to the parent user story\n" \
    "Description: Detailed explanation of the technical work required\n" \
    "Acceptance Criteria: Specific requirements that must be met for completion\n" \
    "Estimated Effort: Time or complexity estimation\n" \
    "Dependencies: Any tasks that must be completed first"
development_engineer_evaluation_agent = EvaluationAgent(open_ai_key, persona_dev_engineer_eval, person_dev_engineer_eval_criteria, development_engineer_knowledge_agent, 5)

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.
def _final_from_evaluation(eval_result, fallback):
    """Pull the validated response out of an EvaluationAgent result dict."""
    if not isinstance(eval_result, dict):
        return fallback
    return eval_result.get("final_response") or eval_result.get("response") or fallback


def product_manager_support_function(query):
    knowledge_response = product_manager_knowledge_agent.respond(query)
    eval_result = product_manager_evaluation_agent.evaluate(knowledge_response)
    return {
        "role": "Product Manager",
        "response": _final_from_evaluation(eval_result, knowledge_response),
    }


def program_manager_support_function(query):
    knowledge_response = program_manager_knowledge_agent.respond(query)
    eval_result = program_manager_evaluation_agent.evaluate(knowledge_response)
    return {
        "role": "Program Manager",
        "response": _final_from_evaluation(eval_result, knowledge_response),
    }


def development_engineer_support_function(query):
    knowledge_response = development_engineer_knowledge_agent.respond(query)
    eval_result = development_engineer_evaluation_agent.evaluate(knowledge_response)
    return {
        "role": "Development Engineer",
        "response": _final_from_evaluation(eval_result, knowledge_response),
    }


# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.
routes = [
    {
        "name": "Product Manager",
        "description": (
            "Responsible for defining product personas and user stories only. "
            "Does not define features or tasks. Does not group stories."
        ),
        "func": lambda user_prompt: product_manager_support_function(user_prompt),
    },
    {
        "name": "Program Manager",
        "description": (
            "Responsible for defining product features by grouping related user "
            "stories. Does not define user stories or engineering tasks."
        ),
        "func": lambda user_prompt: program_manager_support_function(user_prompt),
    },
    {
        "name": "Development Engineer",
        "description": (
            "Responsible for defining detailed engineering tasks required to "
            "implement user stories. Does not define stories or features."
        ),
        "func": lambda user_prompt: development_engineer_support_function(user_prompt),
    },
]

routing_agent = RoutingAgent(open_ai_key, routes)

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = (
    "What is the complete product plan for the Email Router? "
    "Generate the user stories, then the product features, and finally "
    "the detailed engineering tasks for the product."
)
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
#   2. Initialize an empty list to store 'completed_steps'.
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
#   4. After the loop, print the final output of the workflow (the last completed step).
if __name__ == "__main__":
    plan = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
    print(f"Extracted {len(plan)} workflow steps from the workflow prompt.")

    completed_steps = []
    for idx, step in enumerate(plan, start=1):
        print(f"\n--- Executing step {idx}/{len(plan)}: {step} ---")
        result = routing_agent.route(step)
        completed_steps.append(result)
        print(f"Result for step {idx}: {result}")

    # Collect results by role so the final output has a user-stories section,
    # a features section, and an engineering-tasks section.
    def _collect(role):
        parts = []
        for r in completed_steps:
            if isinstance(r, dict) and r.get("role") == role and r.get("response"):
                parts.append(str(r["response"]).strip())
        return "\n\n".join(parts) if parts else "(no output generated for this role)"

    user_stories_section = _collect("Product Manager")
    features_section = _collect("Program Manager")
    tasks_section = _collect("Development Engineer")

    final_output = (
        "\n============================================================\n"
        "         EMAIL ROUTER — FINAL PROJECT PLAN\n"
        "============================================================\n\n"
        "------------------------------------------------------------\n"
        "1. USER STORIES (Product Manager)\n"
        "------------------------------------------------------------\n"
        f"{user_stories_section}\n\n"
        "------------------------------------------------------------\n"
        "2. PRODUCT FEATURES (Program Manager)\n"
        "------------------------------------------------------------\n"
        f"{features_section}\n\n"
        "------------------------------------------------------------\n"
        "3. ENGINEERING TASKS (Development Engineer)\n"
        "------------------------------------------------------------\n"
        f"{tasks_section}\n"
        "============================================================\n"
    )

    print("\n*** Workflow execution completed ***")
    print(final_output)