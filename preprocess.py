import string


def clean_text(text):
    """Prepare text before generating BERT embeddings."""
    if text is None:
        return ""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    text = " ".join(words)
    return text


def format_skills(skills):
    """Converts a list of skills or comma-separated string into one clean string."""
    if skills is None:
        return ""
    if isinstance(skills, list):
        skills = " ".join(skills)
    else:
        skills = skills.replace(",", " ")

    words = skills.split()
    return " ".join(words)


def validate_text(text):
    """Returns False if text is empty or only whitespace."""
    if not text or text.strip() == "":
        return False
    return True


def prepare_seeker_input(text):
    """Full preprocessing pipeline for seeker requests."""
    if not validate_text(text):
        return None
    return clean_text(text)


def prepare_provider_input(skills):
    """Full preprocessing pipeline for provider skills."""
    formatted = format_skills(skills)
    cleaned = clean_text(formatted)
    if not validate_text(cleaned):
        return None
    return cleaned
