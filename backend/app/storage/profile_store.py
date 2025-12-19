"""
Stockage des profils utilisateur (MVP: fichiers JSON).
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from ..models.profile import ProfileCreate, ProfileUpdate, UserProfile


class ProfileStore:
    """Stockage des profils en fichiers JSON."""
    
    def __init__(self, data_dir: str = "data/profiles"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, user_id: str) -> Path:
        """Chemin du fichier pour un user_id."""
        # Sanitize user_id pour nom de fichier
        safe_id = user_id.replace("@", "_").replace("/", "_").replace("\\", "_")
        return self.data_dir / f"{safe_id}.json"
    
    def create(self, profile_data: ProfileCreate) -> UserProfile:
        """Créer un nouveau profil."""
        profile = UserProfile(
            id=str(uuid4()),
            user_id=profile_data.user_id,
            full_name=profile_data.full_name,
            email=profile_data.email,
            phone=profile_data.phone,
            location=profile_data.location,
            cv_text=profile_data.cv_text,
            cv_structured=profile_data.cv_structured,
            preferred_contract_types=profile_data.preferred_contract_types,
            preferred_remote=profile_data.preferred_remote,
            salary_min=profile_data.salary_min,
            preferred_countries=profile_data.preferred_countries,
            preferred_categories=profile_data.preferred_categories,
        )
        
        self._save(profile)
        return profile
    
    def get(self, user_id: str) -> UserProfile | None:
        """Récupérer un profil par user_id."""
        file_path = self._get_file_path(user_id)
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convertir les dates string en datetime
                if "created_at" in data:
                    data["created_at"] = datetime.fromisoformat(data["created_at"])
                if "updated_at" in data:
                    data["updated_at"] = datetime.fromisoformat(data["updated_at"])
                return UserProfile(**data)
        except Exception as e:
            print(f"[ProfileStore] Error loading profile {user_id}: {e}")
            return None
    
    def update(self, user_id: str, update_data: ProfileUpdate) -> UserProfile | None:
        """Mettre à jour un profil."""
        profile = self.get(user_id)
        if not profile:
            return None
        
        # Mettre à jour les champs fournis
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            if value is not None:
                setattr(profile, key, value)
        
        profile.updated_at = datetime.now()
        self._save(profile)
        return profile
    
    def delete(self, user_id: str) -> bool:
        """Supprimer un profil."""
        file_path = self._get_file_path(user_id)
        if file_path.exists():
            try:
                file_path.unlink()
                return True
            except Exception as e:
                print(f"[ProfileStore] Error deleting profile {user_id}: {e}")
                return False
        return False
    
    def _save(self, profile: UserProfile) -> None:
        """Sauvegarder un profil."""
        file_path = self._get_file_path(profile.user_id)
        try:
            # Convertir en dict avec dates en ISO string
            data = profile.model_dump()
            data["created_at"] = data["created_at"].isoformat()
            data["updated_at"] = data["updated_at"].isoformat()
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ProfileStore] Error saving profile {profile.user_id}: {e}")
            raise


# Instance globale
profile_store = ProfileStore()

