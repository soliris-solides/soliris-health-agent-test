from typing import Dict
from llm.model import llm

def get_emphatic_message(message: str) -> str:
    """
    Function to maintain a conversation with user based on the provided health problem.

    Args:
         message (str): Contains the users message with problem.
            
    Returns:
        str: Contains an empathetic response.
    """
        
    prompt = f"Analyze: {message} and provide a kind and emphatic message for the user to help them deal with the situation."
    response = llm.invoke(prompt)
    return response.content

def get_advices(query_input: str) -> str:
    """
    Function to provide health advice and guidance.

    Args:
         query_input (str): Contains the user's health problem.
            
    Returns:
        str: Contains advice and guidance.
    """
        
    prompt = f"""Analyze the following query: {query_input}
        Provide kind messege with practical and detailed advice on how to address the described situation. Include activity suggestions, self-care practices, and ways to improve emotional well-being.
        Offer suggestions to relieve symptoms, improve mood, and cope with anxiety or sadness, if mentioned in the problem.
        Don't send big texts.
    """
    response = llm.invoke(prompt)
    return response.content

def get_activities(problem_type: str) -> Dict[str, str]:
    """
    Function to suggest activities or exercises based on the provided health problem.

    Args:
         problem_type (str): Contains the health problem type.
            
    Returns:
        Dict: Contains the suggested activities or exercises.
    """
    
    from llm.model import llm
    
    prompt = f"Analyze: {problem_type} and suggest activities and/or exercises to help address the problem."
    activities_suggested = llm.invoke(prompt)
    
    return activities_suggested.content