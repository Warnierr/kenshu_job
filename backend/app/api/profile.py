"""
Endpoints API pour la gestion des profils utilisateur.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from ..models.profile import ProfileCreate, ProfileUpdate, UserProfile
from ..services.cv_parser import cv_parser
from ..storage.profile_store import profile_store


class ParseCVRequest(BaseModel):
    """Requête pour parser un CV."""
    cv_text: str

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.post("", response_model=UserProfile, status_code=201)
def create_profile(profile_data: ProfileCreate) -> UserProfile:
    """Créer un nouveau profil utilisateur."""
    # Vérifier si profil existe déjà
    existing = profile_store.get(profile_data.user_id)
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    # Parser CV si texte fourni
    profile = profile_store.create(profile_data)
    
    if profile_data.cv_text:
        parsed = cv_parser.parse_text(profile_data.cv_text)
        # Mettre à jour avec données parsées
        update_data = ProfileUpdate(**parsed)
        profile = profile_store.update(profile.user_id, update_data)
    
    return profile


@router.get("/{user_id}", response_model=UserProfile)
def get_profile(user_id: str) -> UserProfile:
    """Récupérer un profil par user_id."""
    profile = profile_store.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/{user_id}", response_model=UserProfile)
def update_profile(user_id: str, update_data: ProfileUpdate) -> UserProfile:
    """Mettre à jour un profil."""
    profile = profile_store.update(user_id, update_data)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Re-parser CV si texte modifié
    if update_data.cv_text is not None and profile.cv_text:
        parsed = cv_parser.parse_text(profile.cv_text)
        # Mettre à jour avec nouvelles données parsées
        parsed_update = ProfileUpdate(**parsed)
        profile = profile_store.update(user_id, parsed_update)
    
    return profile


@router.delete("/{user_id}", status_code=204)
def delete_profile(user_id: str) -> None:
    """Supprimer un profil."""
    success = profile_store.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.post("/{user_id}/parse-cv", response_model=dict)
def parse_cv(user_id: str, request: ParseCVRequest) -> dict:
    """Parser un CV texte et retourner les données extraites."""
    parsed = cv_parser.parse_text(request.cv_text)
    return parsed


@router.post("/{user_id}/upload-cv", response_model=UserProfile)
async def upload_cv(user_id: str, file: UploadFile = File(...)) -> UserProfile:
    """Upload un fichier CV (PDF/DOCX) et parser."""
    # Vérifier le type de fichier
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["pdf", "docx", "doc", "txt"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Supported: pdf, docx, doc, txt"
        )
    
    # Lire le contenu
    content = await file.read()
    
    # Pour MVP: traiter seulement les fichiers texte
    # TODO: Ajouter parsing PDF/DOCX avec bibliothèques dédiées
    if ext == "txt":
        cv_text = content.decode("utf-8", errors="ignore")
    else:
        # Pour l'instant, on stocke juste le fichier
        # TODO: Parser PDF/DOCX
        raise HTTPException(
            status_code=501,
            detail="PDF/DOCX parsing not yet implemented. Please use text format."
        )
    
    # Mettre à jour le profil avec le CV
    profile = profile_store.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = ProfileUpdate(cv_text=cv_text)
    profile = profile_store.update(user_id, update_data)
    
    # Parser le CV
    if profile:
        parsed = cv_parser.parse_text(cv_text)
        parsed_update = ProfileUpdate(**parsed)
        profile = profile_store.update(user_id, parsed_update)
    
    return profile

