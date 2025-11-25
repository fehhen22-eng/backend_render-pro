import re
import unicodedata


def slugify(text: str) -> str:
    """
    Normaliza o nome do time para formato slug.
    Exemplo: "Manchester United" -> "manchester-united"
    Exemplo: "real_madrid" -> "real-madrid"
    """
    if not text:
        return ""
    
    # Normaliza caracteres Unicode
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Converte para minúsculas
    text = text.lower()
    
    # Remove caracteres especiais (mantém letras, números, espaços e hífens)
    text = re.sub(r'[^\w\s-]', '', text)
    
    # Substitui underscores e espaços por hífens
    text = text.replace('_', '-')
    text = re.sub(r'[-\s]+', '-', text)
    text = text.strip('-')
    
    return text


def normalize_team_name(team_name: str) -> str:
    """
    Normaliza o nome do time para comparação e busca.
    """
    return slugify(team_name)


def get_team_filename(team_name: str) -> str:
    """
    Retorna o nome do arquivo CSV para um time.
    Exemplo: "Manchester United" -> "manchester-united.csv"
    """
    return f"{slugify(team_name)}.csv"
