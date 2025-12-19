"""
Service de parsing de CV (texte et fichiers).
"""
from __future__ import annotations

import re
from typing import Any


class CVParser:
    """Parser de CV pour extraire compétences, expérience, etc."""
    
    # Patterns pour extraction
    SKILL_PATTERNS = [
        r"\b(python|java|javascript|typescript|react|vue|angular|node\.?js|go|golang|rust|c\+\+|c#|php|ruby|swift|kotlin|dart|scala|clojure|haskell|elixir|erlang)\b",
        r"\b(kubernetes|docker|terraform|ansible|jenkins|gitlab|github|aws|azure|gcp|cloud)\b",
        r"\b(postgresql|mysql|mongodb|redis|elasticsearch|kafka|rabbitmq|sql|nosql)\b",
        r"\b(react|vue|angular|svelte|next\.?js|nuxt|gatsby|remix)\b",
        r"\b(machine learning|ml|ai|deep learning|nlp|computer vision|tensorflow|pytorch)\b",
        r"\b(devops|sre|ci/cd|agile|scrum|kanban)\b",
    ]
    
    EXPERIENCE_PATTERNS = [
        r"(\d+)\s*(?:ans?|years?|années?)\s*(?:d'?expérience|of experience|exp)",
        r"expérience\s*:\s*(\d+)",
        r"(\d+)\+?\s*(?:ans?|years?)",
    ]
    
    LANGUAGE_PATTERNS = [
        r"\b(anglais|english|français|french|allemand|german|espagnol|spanish|italien|italian|chinois|chinese|japonais|japanese)\b",
    ]
    
    LEVEL_PATTERNS = [
        (r"\b(junior|débutant|beginner|entry)\b", "Junior"),
        (r"\b(mid|intermédiaire|intermediate|confirmé)\b", "Mid"),
        (r"\b(senior|expert|lead|architect|principal)\b", "Senior"),
    ]
    
    def parse_text(self, cv_text: str) -> dict[str, Any]:
        """Parser un CV en texte pour extraire les informations."""
        text_lower = cv_text.lower()
        
        # Extraire compétences
        skills = self._extract_skills(text_lower)
        
        # Extraire années d'expérience
        experience_years = self._extract_experience(cv_text)
        
        # Extraire niveau
        experience_level = self._extract_level(text_lower)
        
        # Extraire langues
        languages = self._extract_languages(text_lower)
        
        # Extraire secteurs (basique)
        sectors = self._extract_sectors(text_lower)
        
        return {
            "skills": skills,
            "experience_years": experience_years,
            "experience_level": experience_level,
            "languages": languages,
            "sectors": sectors,
        }
    
    def _extract_skills(self, text: str) -> list[str]:
        """Extraire les compétences techniques."""
        skills = set()
        
        for pattern in self.SKILL_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                skill = match.lower() if isinstance(match, str) else match[0].lower()
                # Normaliser
                skill = skill.replace(".", "").replace(" ", "")
                if len(skill) > 2:  # Filtrer les matches trop courts
                    skills.add(skill)
        
        return sorted(list(skills))
    
    def _extract_experience(self, text: str) -> int | None:
        """Extraire les années d'expérience."""
        for pattern in self.EXPERIENCE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                years = int(match.group(1))
                # Limiter à 50 ans (réaliste)
                return min(years, 50)
        return None
    
    def _extract_level(self, text: str) -> str | None:
        """Extraire le niveau d'expérience."""
        for pattern, level in self.LEVEL_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return level
        return None
    
    def _extract_languages(self, text: str) -> list[str]:
        """Extraire les langues."""
        languages = set()
        
        for pattern in self.LANGUAGE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                lang = match.lower()
                # Normaliser
                lang_map = {
                    "anglais": "Anglais",
                    "english": "Anglais",
                    "français": "Français",
                    "french": "Français",
                    "allemand": "Allemand",
                    "german": "Allemand",
                    "espagnol": "Espagnol",
                    "spanish": "Espagnol",
                }
                languages.add(lang_map.get(lang, lang.capitalize()))
        
        return sorted(list(languages))
    
    def _extract_sectors(self, text: str) -> list[str]:
        """Extraire les secteurs d'activité (basique)."""
        sectors = []
        
        sector_keywords = {
            "fintech": ["fintech", "finance", "banking", "banque"],
            "e-commerce": ["e-commerce", "ecommerce", "retail", "commerce"],
            "healthcare": ["healthcare", "santé", "médical", "health"],
            "edtech": ["edtech", "éducation", "education", "formation"],
            "saas": ["saas", "software as a service"],
            "gaming": ["gaming", "jeu", "game"],
        }
        
        for sector, keywords in sector_keywords.items():
            if any(keyword in text for keyword in keywords):
                sectors.append(sector)
        
        return sectors


# Instance globale
cv_parser = CVParser()

