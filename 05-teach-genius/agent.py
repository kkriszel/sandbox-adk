from google.adk.agents import LlmAgent, Agent
from google.adk.tools import google_search, agent_tool

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

# --- Dedicated Agent for search; workaround because one tool call can be done at a time ---
search_agent = Agent(
    name='search_agent',
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="You're a spealist in Google Search",
    tools=[google_search],
)

# -- 1. Agent: material description --
material_description_agent = LlmAgent(
    name="material_description_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    description="A helpful assistant that can describe teaching materials.",
    instruction="You are a helpful assistant that can describe teaching materials. "
                "Your output should be a lesson plan for the given material. "
                "You should focus on providing lesson structure, objectives, and details about the material.",
    tools=[agent_tool.AgentTool(agent=search_agent)],
    output_key="material_description",
)

# -- 2. Agent: interactive lesson question generation --
interactive_lesson_question_generation_agent = LlmAgent(
    name="interactive_lesson_question_generation_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    description="A helpful assistant that can generate interactive lesson questions.",
    instruction="You are a helpful assistant that can generate interactive lesson questions. "
                "The lesson description is provided in state['material_description']. "
                "Your output should be a list of quizz-like questions that are interactive and engaging. "
                "Each question could have multiple choice answers.",
    tools=[agent_tool.AgentTool(agent=search_agent)],
    output_key="interactive_lesson_questions",
)

# -- 3. Agent: interactive lesson visualization planner --
interactive_lesson_visualization_planner_agent = LlmAgent(
    name="interactive_lesson_visualization_planner_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    description="A helpful assistant that can plan the visualization of an interactive lesson.",
    instruction="You are a helpful assistant that can plan the visualization of an interactive lesson. "
                "The lesson description is provided in state['material_description']. "
                "The lesson questions are provided in state['interactive_lesson_questions']. "
                "Your output should be a list of visualization ideas that can be used to visualize the lesson. "
                "Each visualization idea should be a short description of the visualization, divided into plans for generating the "
                "necessary assets (e.g. images, svgs, css, etc.).",
    output_key="interactive_lesson_visualization_plan",
)

# # -- 4. Agent: interactive lesson visualization generation --
# interactive_lesson_visualization_generation_agent = LlmAgent(
#     name="interactive_lesson_visualization_generation_agent",
#     model=MODEL_GEMINI_2_0_FLASH,
#     description="A helpful assistant that can generate the assets for an interactive lesson visualization.",
#     instruction="You are a helpful assistant that can generate the assets for an interactive lesson visualization. "
#                 "The visualization plan is provided in state['interactive_lesson_visualization_plan']. "
#                 "Your output should be the assets that can be used to create the visualization. ",
# )

# -- 4. Agent: html generation --
html_generation_agent = LlmAgent(
    name="html_generation_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    description="A helpful assistant that can generate HTML code.",
    instruction="You are a helpful assistant that can generate HTML code. "
                "The visualization plan is provided in state['interactive_lesson_visualization_plan']. "
                "Your output should be the whole HTML code, without placeholders, that can be used to create the visualization. ",
    tools=[agent_tool.AgentTool(agent=search_agent)],
    output_key="html_code",
)

root_agent = Agent(
    name="root_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    description="A helpful assistant that can generate a lesson plan, interactive lesson questions, and a visualization plan for an interactive lesson.",
    instruction="You are a helpful assistant that can generate a lesson plan, interactive lesson questions, and a visualization plan for an interactive lesson. "
                "You should use the 'material_description_agent' to generate the lesson plan, "
                "the 'interactive_lesson_question_generation_agent' to generate the interactive lesson questions, "
                "the 'interactive_lesson_visualization_planner_agent' to generate the visualization plan, "
                "and the 'html_generation_agent' to generate the HTML code.",
    sub_agents=[material_description_agent, interactive_lesson_question_generation_agent, interactive_lesson_visualization_planner_agent, html_generation_agent],
)
