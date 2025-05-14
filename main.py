import os
import re
from rich.console import Console
from rich.panel import Panel
from datetime import datetime
import json
from llm_api import MistralProvider
from tavily import TavilyClient

# Set Tavily API key
os.environ["TAVILY_API_KEY"] = "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"

# Set environment variables for Mistral API key
os.environ["MISTRAL_API_KEY"] = "jKULZ0T9q0KcxZNq0Y4FoQ8QxDjY4OAy"

# Define the models to be used for each stage
ORCHESTRATOR_MODEL = "mistral-large-latest"
SUB_AGENT_MODEL = "mistral-large-latest"
REFINER_MODEL = "mistral-large-latest"

# Initialize the Rich Console
console = Console()

def gpt_orchestrator(objective, file_content=None, previous_results=None, use_search=False):
    console.print(f"
[bold]Calling Orchestrator for your objective[/bold]")
    previous_results_text = "\n".join(previous_results) if previous_results else "None"
    if file_content:
        console.print(Panel(f"File content:\n{file_content}", title="[bold blue]File Content[/bold blue]", title_align="left", border_style="blue"))
    
    # Initialize Mistral Provider
    mistral = MistralProvider(config={'model': ORCHESTRATOR_MODEL})
    
    messages = [
        {"role": "system", "content": "You are a detailed and meticulous assistant. Your primary goal is to break down complex objectives into manageable sub-tasks, provide thorough reasoning, and ensure code correctness. Always explain your thought process step-by-step and validate any code for errors, improvements, and adherence to best practices."},
        {"role": "user", "content": f"Based on the following objective{' and file content' if file_content else ''}, and the previous sub-task results (if any), please break down the objective into the next sub-task, and create a concise and detailed prompt for a subagent so it can execute that task. IMPORTANT!!! when dealing with code tasks make sure you check the code for errors and provide fixes and support as part of the next sub-task. If you find any bugs or have suggestions for better code, please include them in the next sub-task prompt. Please assess if the objective has been fully achieved. If the previous sub-task results comprehensively address all aspects of the objective, include the phrase 'The task is complete:' at the beginning of your response. If the objective is not yet fully achieved, break it down into the next sub-task and create a concise and detailed prompt for a subagent to execute that task.:\n\nObjective: {objective}" + ('\nFile content:\n' + file_content if file_content else '') + f"\n\nPrevious sub-task results:\n{previous_results_text}"}
    ]

    if use_search:
        messages.append({"role": "user", "content": "Please also generate a JSON object containing a single 'search_query' key, which represents a question that, when asked online, would yield important information for solving the subtask. The question should be specific and targeted to elicit the most relevant and helpful resources. Format your JSON like this, with no additional text before or after:\n{\"search_query\": \"<question>\"}\n"})

    response_text = mistral.chat_completion(messages)

    console.print(Panel(response_text, title=f"[bold green]Orchestrator[/bold green]", title_align="left", border_style="green", subtitle="Sending task to sub-agent 👇"))

    search_query = None
    if use_search:
        json_match = re.search(r'{.*}', response_text, re.DOTALL)
        if json_match:
            json_string = json_match.group()
            try:
                search_query = json.loads(json_string)["search_query"]
                tavily_api_key = os.environ.get("TAVILY_API_KEY")
                if not tavily_api_key:
                    console.print("[bold red]Warning: Tavily API key not found. Skipping web search.[/bold red]")
                    search_query = None
                else:
                    console.print(Panel(f"Search Query: {search_query}", title="[bold blue]Search Query[/bold blue]", title_align="left", border_style="blue"))
                    response_text = response_text.replace(json_string, "").strip()
            except json.JSONDecodeError as e:
                console.print(Panel(f"Error parsing JSON: {e}", title="[bold red]JSON Parsing Error[/bold red]", title_align="left", border_style="red"))
                console.print(Panel(f"Skipping search query extraction.", title="[bold yellow]Search Query Extraction Skipped[/bold yellow]", title_align="left", border_style="yellow"))
        else:
            search_query = None

    return response_text, file_content, search_query

def gpt_sub_agent(prompt, search_query=None, previous_gpt_tasks=None, use_search=False, continuation=False):
    console.print(f"
[bold]Calling Sub-Agent[/bold]")
    
    # Initialize Mistral Provider
    mistral = MistralProvider(config={'model': SUB_AGENT_MODEL})
    
    if search_query and use_search:
        tavily_api_key = os.environ.get("TAVILY_API_KEY")
        if not tavily_api_key:
            console.print("[bold red]Warning: Tavily API key not found. Skipping web search.[/bold red]")
            search_query = None
        else:
            tavily = TavilyClient(api_key=tavily_api_key)
            search_results = tavily.search(query=search_query, max_results=5)
            context = "\n".join([result['content'] for result in search_results['results']])
            prompt += f"\n\nAdditional Context from Web Search:\n{context}"
    
    messages = [
        {"role": "system", "content": "You are a highly capable sub-agent specializing in executing specific tasks with precision, creativity, and attention to detail. Your goal is to solve the given sub-task comprehensively and produce high-quality output."},
        {"role": "user", "content": prompt}
    ]

    if previous_gpt_tasks:
        messages.insert(1, {"role": "user", "content": f"Previous task results:\n{previous_gpt_tasks}"})

    if continuation:
        messages.insert(1, {"role": "user", "content": "This is a continuation of a previous task. Please review the context and continue from where the last task left off."})