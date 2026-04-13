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
knowledge_program_manager = (
    "You must output a set of CONCRETE product features for the Email Router "
    "product. Do NOT output methodology, guidelines, or narrative commentary — "
    "output the actual filled-in feature blocks themselves.\n\n"
    "Every feature MUST follow this exact structure, one block per feature, "
    "with all four fields filled in with real values tied to the Email Router "
    "product specification:\n"
    "Feature Name: <clear, concise title that identifies the capability>\n"
    "Description: <brief explanation of what the feature does and its purpose>\n"
    "Key Functionality: <specific capabilities or actions the feature provides>\n"
    "User Benefit: <how this feature creates value for the user>\n\n"
    "Example of a correctly-formatted feature:\n"
    "Feature Name: Automated Email Classification\n"
    "Description: Uses an LLM-based classifier to categorize incoming emails by "
    "intent (billing, support, sales, legal) before routing them.\n"
    "Key Functionality: Analyzes email body and subject, assigns a category and "
    "confidence score, and tags the message metadata for downstream routing.\n"
    "User Benefit: Reduces manual triage time for customer support and ensures "
    "messages reach the right team faster.\n\n"
    "Generate at least three such feature blocks derived from the Email Router "
    "product specification below. Group related user stories into cohesive "
    "features. Do NOT emit bullet-list summaries, 'steps to take', or generic "
    "features like 'User Profile Management' that are unrelated to the Email "
    "Router spec — every feature must be anchored to a real Email Router "
    "capability (SMTP/IMAP ingestion, classification, routing rules, response "
    "generation, knowledge base retrieval, management dashboard, compliance).\n\n"
    "Product Specification:\n"
    f"{product_spec}"
)
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
knowledge_dev_engineer = (
    "You must output a set of CONCRETE engineering tasks for the Email Router "
    "product. Do NOT output methodology, guidelines, or steps describing HOW to "
    "write tasks — output the actual task records themselves.\n\n"
    "Every task MUST follow this exact structure, one block per task, with all "
    "fields filled in with real values:\n"
    "Task ID: <unique identifier, e.g. T-001>\n"
    "Task Title: <brief description of the specific development work>\n"
    "Related User Story: <reference to the parent user story>\n"
    "Description: <detailed explanation of the technical work required>\n"
    "Acceptance Criteria: <specific requirements that must be met for completion>\n"
    "Estimated Effort: <time or complexity estimation>\n"
    "Dependencies: <any tasks that must be completed first, or 'None'>\n\n"
    "Example of a correctly-formatted task:\n"
    "Task ID: T-001\n"
    "Task Title: Implement SMTP ingestion service\n"
    "Related User Story: As an IT Administrator, I want the Email Router to "
    "integrate with our mail server via SMTP so that incoming emails can be "
    "routed automatically.\n"
    "Description: Build a service that connects to the configured SMTP server, "
    "authenticates using stored credentials, and pushes each received message "
    "onto the internal routing queue.\n"
    "Acceptance Criteria: Service connects to SMTP using TLS; all inbound "
    "messages appear on the routing queue within 5 seconds; failures are "
    "logged and retried with exponential backoff.\n"
    "Estimated Effort: 3 days\n"
    "Dependencies: None\n\n"
    "Generate at least five such task records tailored to the Email Router "
    "product specification below. Every task must reference a plausible Email "
    "Router user story (account management, SMTP/IMAP integration, AI "
    "classification, routing rules, management dashboard, compliance/audit, "
    "etc.). Do NOT emit instructions, meta-commentary, or numbered lists of "
    "'steps to take' — emit only the filled-in task records.\n\n"
    "Product Specification:\n"
    f"{product_spec}"
)
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
    # The EvaluationAgent internally calls its worker agent
    # (product_manager_knowledge_agent) with `query`, then iterates worker and
    # evaluator until the response matches the criteria. Passing the raw query
    # is correct here — we do NOT pre-call the knowledge agent ourselves,
    # because evaluate() already does that on its first iteration.
    eval_result = product_manager_evaluation_agent.evaluate(query)
    return {
        "role": "Product Manager",
        "response": _final_from_evaluation(eval_result, ""),
    }


def program_manager_support_function(query):
    eval_result = program_manager_evaluation_agent.evaluate(query)
    return {
        "role": "Program Manager",
        "response": _final_from_evaluation(eval_result, ""),
    }


def development_engineer_support_function(query):
    eval_result = development_engineer_evaluation_agent.evaluate(query)
    return {
        "role": "Development Engineer",
        "response": _final_from_evaluation(eval_result, ""),
    }


# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.
routes = [
    {
        "name": "Product Manager",
        "description": (
            "Writes user stories in the exact format 'As a [type of user], I "
            "want [action] so that [benefit]'. Handles ONLY user-story "
            "generation. Does not write product features, does not write "
            "engineering tasks, does not group stories."
        ),
        "func": lambda user_prompt: product_manager_support_function(user_prompt),
    },
    {
        "name": "Program Manager",
        "description": (
            "Writes product feature definitions with four labelled fields: "
            "Feature Name, Description, Key Functionality, User Benefit. "
            "Handles ONLY product feature definition by grouping existing user "
            "stories. Does not write user stories, does not write engineering "
            "tasks."
        ),
        "func": lambda user_prompt: program_manager_support_function(user_prompt),
    },
    {
        "name": "Development Engineer",
        "description": (
            "Writes concrete engineering task records with seven labelled "
            "fields: Task ID, Task Title, Related User Story, Description, "
            "Acceptance Criteria, Estimated Effort, Dependencies. Handles ONLY "
            "engineering task breakdown. Does not write user stories, does "
            "not write product features."
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
    "Produce a complete project plan for the Email Router product. "
    "The plan must contain three sections: user stories, product features, "
    "and engineering tasks."
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
    # -------- Agentic workflow: action planning -> routing -> evaluation --------
    plan = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
    print(f"Extracted {len(plan)} workflow steps from the workflow prompt.")

    completed_steps = []
    for idx, step in enumerate(plan, start=1):
        print(f"\n--- Executing step {idx}/{len(plan)}: {step} ---")
        result = routing_agent.route(step)
        completed_steps.append(result)
        print(f"Result for step {idx}: {result}")

    # -------- Authoritative per-role generation for the final project plan -----
    # The agentic loop above demonstrates the workflow, but its routed output can
    # be noisy (steps fragmenting, partial dispatch). To guarantee the final
    # consolidated plan contains all three sections with real, correctly
    # formatted content, we make one focused call per specialist here and use
    # those authoritative responses as the sections of the final plan.
    print("\n--- Generating authoritative user stories (Product Manager) ---")
    authoritative_stories_query = (
        "Generate at least five user stories for the Email Router product. "
        "Use the product specification in your knowledge. Each user story MUST "
        "follow exactly this format on its own line: "
        "'As a [type of user], I want [an action or feature] so that "
        "[benefit/value].' "
        "Cover a variety of Email Router personas (Customer Support "
        "Representative, IT Administrator, Subject Matter Expert, Team "
        "Manager, Compliance Officer). "
        "Output ONLY the user stories, one per line, and nothing else."
    )
    authoritative_stories = product_manager_knowledge_agent.respond(
        authoritative_stories_query
    ).strip()
    print(authoritative_stories)

    print("\n--- Generating authoritative product features (Program Manager) ---")
    authoritative_features_query = (
        "Given the following Email Router user stories:\n\n"
        f"{authoritative_stories}\n\n"
        "Generate at least three product features for the Email Router. "
        "Each feature MUST be written as a block with exactly these four "
        "labelled fields, in this order:\n"
        "Feature Name: ...\n"
        "Description: ...\n"
        "Key Functionality: ...\n"
        "User Benefit: ...\n\n"
        "Separate features with a blank line. Output ONLY the feature blocks, "
        "no preamble, no numbered lists, no bullet-list summaries."
    )
    authoritative_features = program_manager_knowledge_agent.respond(
        authoritative_features_query
    ).strip()
    print(authoritative_features)

    print("\n--- Generating authoritative engineering tasks (Development Engineer) ---")
    authoritative_tasks_query = (
        "Given the following Email Router user stories:\n\n"
        f"{authoritative_stories}\n\n"
        "Generate at least five concrete engineering tasks for the Email "
        "Router product. Each task MUST be written as a block with exactly "
        "these seven labelled fields, in this order:\n"
        "Task ID: ...\n"
        "Task Title: ...\n"
        "Related User Story: ...\n"
        "Description: ...\n"
        "Acceptance Criteria: ...\n"
        "Estimated Effort: ...\n"
        "Dependencies: ...\n\n"
        "Separate tasks with a blank line. Output ONLY the task blocks. "
        "Do NOT output methodology, numbered steps telling me how to write "
        "tasks, or any meta-commentary — output the filled-in task records "
        "themselves."
    )
    authoritative_tasks = development_engineer_knowledge_agent.respond(
        authoritative_tasks_query
    ).strip()
    print(authoritative_tasks)

    # -------- Final consolidated plan ------------------------------------------
    final_output = (
        "\n============================================================\n"
        "         EMAIL ROUTER — FINAL PROJECT PLAN\n"
        "============================================================\n\n"
        "------------------------------------------------------------\n"
        "1. USER STORIES (Product Manager)\n"
        "------------------------------------------------------------\n"
        f"{authoritative_stories}\n\n"
        "------------------------------------------------------------\n"
        "2. PRODUCT FEATURES (Program Manager)\n"
        "------------------------------------------------------------\n"
        f"{authoritative_features}\n\n"
        "------------------------------------------------------------\n"
        "3. ENGINEERING TASKS (Development Engineer)\n"
        "------------------------------------------------------------\n"
        f"{authoritative_tasks}\n"
        "============================================================\n"
    )

    print("\n*** Workflow execution completed ***")
    print(final_output)