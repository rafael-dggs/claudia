import tiktoken

def chunk_text(text: str, max_completion_tokens: int = 1000, overlap: int = 150) -> list[str]:
    """
    Divide um texto longo em chunks menores preservando limites de tokens e adicionando sobreposição.
    """
    # Usa o encoding padrão para a maioria dos modelos OpenAI
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    
    chunks = []
    start = 0
    
    while start < len(tokens):
        end = min(start + max_completion_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        
        # Avança o ponteiro, recuando o valor do overlap (exceto no último chunk)
        start += (max_completion_tokens - overlap)
        
    return chunks