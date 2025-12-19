"""
Modèle de profil utilisateur avec CV.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """Profil utilisateur avec CV."""
    
    id: str = Field(..., description="UUID du profil")
    user_id: str = Field(..., description="Identifiant utilisateur (email ou UUID)")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Informations personnelles
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None  # Ville, Pays
    
    # CV (3 formats possibles)
    cv_text: str | None = Field(None, description="CV en texte libre")
    cv_file_path: str | None = Field(None, description="Chemin vers fichier CV uploadé")
    cv_structured: dict[str, Any] | None = Field(None, description="CV structuré (formulaire)")
    
    # Données extraites du CV (pour scoring)
    skills: list[str] = Field(default_factory=list, description="Compétences techniques")
    experience_years: int | None = None
    experience_level: str | None = None  # Junior, Mid, Senior
    sectors: list[str] = Field(default_factory=list, description="Secteurs d'activité")
    languages: list[str] = Field(default_factory=list, description="Langues parlées")
    education: list[dict[str, Any]] = Field(default_factory=list, description="Formation")
    
    # Préférences de recherche
    preferred_contract_types: list[str] = Field(default_factory=list)
    preferred_remote: str | None = None  # remote, hybrid, onsite
    salary_min: int | None = None
    preferred_countries: list[str] = Field(default_factory=list)
    preferred_categories: list[str] = Field(default_factory=list)
    
    def to_cv_summary(self) -> str:
        """Convertir le profil en résumé CV pour scoring."""
        parts = []
        
        if self.skills:
            parts.append(f"Compétences: {', '.join(self.skills)}")
        
        if self.experience_years:
            parts.append(f"{self.experience_years} ans d'expérience")
        
        if self.experience_level:
            parts.append(f"Niveau: {self.experience_level}")
        
        if self.sectors:
            parts.append(f"Secteurs: {', '.join(self.sectors)}")
        
        if self.languages:
            parts.append(f"Langues: {', '.join(self.languages)}")
        
        if self.cv_text:
            # Prendre les 200 premiers caractères du CV texte
            parts.append(self.cv_text[:200])
        
        return " | ".join(parts) if parts else ""


class ProfileCreate(BaseModel):
    """Modèle pour création de profil."""
    user_id: str
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    cv_text: str | None = None
    cv_structured: dict[str, Any] | None = None
    preferred_contract_types: list[str] = Field(default_factory=list)
    preferred_remote: str | None = None
    salary_min: int | None = None
    preferred_countries: list[str] = Field(default_factory=list)
    preferred_categories: list[str] = Field(default_factory=list)


class ProfileUpdate(BaseModel):
    """Modèle pour mise à jour de profil."""
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    cv_text: str | None = None
    cv_structured: dict[str, Any] | None = None
    skills: list[str] | None = None
    experience_years: int | None = None
    experience_level: str | None = None
    sectors: list[str] | None = None
    languages: list[str] | None = None
    education: list[dict[str, Any]] | None = None
    preferred_contract_types: list[str] | None = None
    preferred_remote: str | None = None
    salary_min: int | None = None
    preferred_countries: list[str] | None = None
    preferred_categories: list[str] | None = None

