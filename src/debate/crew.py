from debate.tools.sendgrid_tool import SendGridEmailTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from debate.tools.web_search_tool import web_search_tool

@CrewBase
class Debate():
    """Debate crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def debater_favor(self) -> Agent:
        return Agent(
            config=self.agents_config['debater_favor'],
            tools=[web_search_tool]
        )
    
    @agent
    def debater_against(self) -> Agent:
        return Agent(
            config=self.agents_config['debater_against'],
            tools=[web_search_tool]
        )
    
    @agent
    def debater_favor_validation(self) -> Agent:
        return Agent(
            config=self.agents_config['debater_favor_validation']
        )

    @agent
    def debater_against_validation(self) -> Agent:
        return Agent(
            config=self.agents_config['debater_against_validation'],
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config['judge']
        )

    @agent
    def sender(self) -> Agent:
        return Agent(
            config=self.agents_config['sender'],
            tools=[SendGridEmailTool()]
        )

    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config['propose'],
        )

    @task
    def propose_validation(self) -> Task:
        return Task(
            config=self.tasks_config['propose_validation'],
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config['oppose'],
        )

    @task
    def oppose_validation(self) -> Task:
        return Task(
            config=self.tasks_config['oppose_validation'],
        )

    @task
    def decide(self) -> Task:
        return Task(
            config=self.tasks_config['decide'],
        )

    @task
    def send_email(self) -> Task:
        return Task(
            config=self.tasks_config['send_email'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
