def get_presentation(content: str) -> str:
    """
    Retorna uma apresentação amigável e focada do assistente.

    Args:
        content (str): Mensagem de apresentação. Por padrão, usa uma versão pré-gerada.

    Returns:
        str: A mensagem de apresentação.
    """
    return content

def get_not_related_message() -> str:
    """
    Retorna uma resposta padrão para quando o tema da conversa não é relacionado à saúde.

    Essa mensagem informa que o assistente é voltado para saúde física e mental, 
    usando emoticons para manter um tom educado e receptivo, e redireciona o usuário
    para tópicos de saúde.

    Returns:
        str: Uma mensagem educada indicando que o assunto não é da área do assistente.
    """
    return "Desculpe, eu sou um assistente de saúde física e mental 😕. Há alguma questão relacionada a saúde que posso te ajudar hoje? 😊"

def get_missing_context_message() -> str:
    """
    Retorna uma resposta quando não há contexto suficiente para continuar a conversa.

    Esta função é usada quando o assistente não consegue compreender ou responder adequadamente
    devido à falta de informações contextuais fornecidas pelo usuário. A mensagem gerada 
    solicita gentilmente mais detalhes para que o assistente possa ajudar de forma eficaz.

    Returns:
        str: Uma mensagem solicitando mais informações ao usuário.
    """
    return "Desculpe, não entendi completamente o que você quis dizer 🤔. Pode me dar mais detalhes para que eu possa te ajudar melhor? 😊"
