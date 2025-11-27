import re
import unicodedata

def slugify(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = text.replace('_', '-')
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def normalize_team_name(team_name: str) -> str:
    return slugify(team_name)


def get_team_filename(team_name: str) -> str:
    return f"{slugify(team_name)}.csv"
