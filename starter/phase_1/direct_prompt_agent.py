# Test script for DirectPromptAgent class

import os
from dotenv import load_dotenv

from starter.phase_1.workflow_agents.base_agents import DirectPromptAgent

# Load environment variables from .env file
load_dotenv()

# TODO: 2 - Load the OpenAI API key from the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the Capital of France?"

# TODO: 3 - Instantiate the DirectPromptAgent as direct_agent
# TODO: 4 - Use direct_agent to send the prompt defined above and store the response
direct_agent = DirectPromptAgent(openai_api_key)

if __name__ == "__main__":
    direct_agent_response = direct_agent.respond(prompt)

    # Print the response from the agent
    print(direct_agent_response)

    # TODO: 5 - Print an explanatory message describing the knowledge source used by the agent to generate the response
    direct_agent_response = direct_agent.respond(f"give me an explanatory message describing the source of the response {direct_agent_response}")
    print(direct_agent_response)
