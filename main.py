from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_experimental.agents import create_csv_agent
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import Tool
from langchain_experimental.tools import PythonREPLTool

load_dotenv()


def main():

    print("Welcome...Booting...")

    python_agent_executor = create_python_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        tool=PythonREPLTool(),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    csv_agent = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        path="employees.csv",
    )

    csv_agent.run("which employee has the highest salary in the employees csv file?")

    grand_agent = initialize_agent(
        tools=[
            Tool(
                name="PythonAgent",
                func=python_agent_executor.run,
                description="""useful for when you NEED to work with Natural Language Processing, 
                and write it from python itself and execute the python code, returning the results 
                of the code exection, DO NOT SEND PYTHON CODE BACK TO THIS TOOL""",
            ),
            Tool(
                name="CSVAgent",
                func=csv_agent.run,
                description="""useful for when you NEED to work with csv files, and answer questinon over emplyee csv file, takes an input the entire qurestion and returns only answer after the pandas calucalations""",
            ),
        ],
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )


if __name__ == "__main__":
    print(main())
