"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";

type UserProfile = {
  id: string;
  user_id: string;
  full_name?: string;
  email?: string;
  phone?: string;
  location?: string;
  cv_text?: string;
  skills: string[];
  experience_years?: number;
  experience_level?: string;
  languages: string[];
  preferred_contract_types: string[];
  preferred_remote?: string;
  salary_min?: number;
  preferred_countries: string[];
  preferred_categories: string[];
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

type TabType = "text" | "upload" | "structured";

export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState<TabType>("text");
  const [userId, setUserId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [profile, setProfile] = useState<UserProfile | null>(null);

  // Form data
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [location, setLocation] = useState("");
  const [cvText, setCvText] = useState("");
  const [preferredRemote, setPreferredRemote] = useState("hybrid");
  const [salaryMin, setSalaryMin] = useState(45000);
  const [preferredCountries, setPreferredCountries] = useState("fr");

  const loadProfile = async (uid: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/profile/${uid}`);
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
        setFullName(data.full_name || "");
        setEmail(data.email || "");
        setPhone(data.phone || "");
        setLocation(data.location || "");
        setCvText(data.cv_text || "");
        setPreferredRemote(data.preferred_remote || "hybrid");
        setSalaryMin(data.salary_min || 45000);
        setPreferredCountries(data.preferred_countries?.join(",") || "fr");
      }
    } catch (err) {
      console.error("Error loading profile:", err);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const profileData = {
        user_id: userId || email || `user_${Date.now()}`,
        full_name: fullName,
        email: email,
        phone: phone,
        location: location,
        cv_text: cvText,
        preferred_remote: preferredRemote,
        salary_min: salaryMin,
        preferred_countries: preferredCountries.split(",").map((c) => c.trim()),
      };

      let res;
      if (profile) {
        // Update existing
        res = await fetch(`${API_BASE}/api/profile/${profile.user_id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(profileData),
        });
      } else {
        // Create new
        res = await fetch(`${API_BASE}/api/profile`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(profileData),
        });
      }

      if (!res.ok) {
        const errData = await res.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(errData.detail || `HTTP ${res.status}`);
      }

      const savedProfile = await res.json();
      setProfile(savedProfile);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      setError(err.message || "Erreur lors de la sauvegarde");
    } finally {
      setLoading(false);
    }
  };

  const handleParseCV = async () => {
    if (!cvText) return;

    setLoading(true);
    try {
      const uid = profile?.user_id || userId || email || `user_${Date.now()}`;
      const res = await fetch(`${API_BASE}/api/profile/${uid}/parse-cv`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cv_text: cvText }),
      });

      if (res.ok) {
        const parsed = await res.json();
        alert(`CV parsé !\nCompétences: ${parsed.skills?.join(", ") || "Aucune"}\nExpérience: ${parsed.experience_years || "N/A"} ans\nNiveau: ${parsed.experience_level || "N/A"}`);
      }
    } catch (err: any) {
      setError(err.message || "Erreur lors du parsing");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div style={{ marginBottom: 24 }}>
        <Link href="/" style={{ color: "var(--neon-cyan)", textDecoration: "none" }}>
          ← Retour à la recherche
        </Link>
      </div>

      <h1>👤 Mon Profil</h1>
      <p className="subtitle">Créez votre profil pour améliorer vos recherches d&apos;emploi</p>

      <div className="card">
        <div style={{ marginBottom: 24 }}>
          <label>
            🔑 Identifiant utilisateur (email ou ID unique)
            <input
              value={userId}
              onChange={(e) => {
                setUserId(e.target.value);
                if (e.target.value) {
                  loadProfile(e.target.value);
                }
              }}
              placeholder="votre.email@example.com"
              style={{ marginTop: 8 }}
            />
          </label>
          {profile && (
            <p style={{ color: "var(--neon-green)", marginTop: 8 }}>
              ✓ Profil trouvé ! Modifiez les champs ci-dessous.
            </p>
          )}
        </div>

        <form onSubmit={handleSubmit}>
          <div className="grid" style={{ marginBottom: 24 }}>
            <label>
              👤 Nom complet
              <input
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Jean Dupont"
              />
            </label>
            <label>
              📧 Email
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="jean.dupont@example.com"
              />
            </label>
            <label>
              📱 Téléphone
              <input
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+33 6 12 34 56 78"
              />
            </label>
            <label>
              📍 Localisation
              <input
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="Paris, France"
              />
            </label>
          </div>

          {/* Tabs pour CV */}
          <div style={{ marginBottom: 24 }}>
            <label style={{ marginBottom: 12, display: "block" }}>📄 CV</label>
            <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
              <button
                type="button"
                className={`category-btn ${activeTab === "text" ? "active" : ""}`}
                onClick={() => setActiveTab("text")}
              >
                Texte libre
              </button>
              <button
                type="button"
                className={`category-btn ${activeTab === "upload" ? "active" : ""}`}
                onClick={() => setActiveTab("upload")}
              >
                Upload fichier
              </button>
              <button
                type="button"
                className={`category-btn ${activeTab === "structured" ? "active" : ""}`}
                onClick={() => setActiveTab("structured")}
              >
                Formulaire
              </button>
            </div>

            {activeTab === "text" && (
              <div>
                <textarea
                  value={cvText}
                  onChange={(e) => setCvText(e.target.value)}
                  placeholder="Collez votre CV ici... (compétences, expérience, formation, etc.)"
                  rows={10}
                  style={{ width: "100%", marginBottom: 8 }}
                />
                <button
                  type="button"
                  onClick={handleParseCV}
                  className="btn"
                  style={{ fontSize: "0.9rem", padding: "8px 16px" }}
                >
                  🔍 Parser le CV
                </button>
              </div>
            )}

            {activeTab === "upload" && (
              <div style={{ padding: 24, border: "2px dashed var(--neon-cyan)", borderRadius: 8 }}>
                <p style={{ color: "var(--text-muted)", marginBottom: 16 }}>
                  Upload de fichier (PDF/DOCX) - Bientôt disponible
                </p>
                <input type="file" accept=".pdf,.docx,.doc,.txt" disabled />
              </div>
            )}

            {activeTab === "structured" && (
              <div style={{ padding: 16, background: "rgba(0, 15, 40, 0.6)", borderRadius: 8 }}>
                <p style={{ color: "var(--text-muted)" }}>
                  Formulaire structuré - Bientôt disponible
                </p>
              </div>
            )}
          </div>

          {/* Préférences */}
          <div className="grid" style={{ marginBottom: 24 }}>
            <label>
              🏠 Remote préféré
              <select value={preferredRemote} onChange={(e) => setPreferredRemote(e.target.value)}>
                <option value="remote">Full remote</option>
                <option value="hybrid">Hybride</option>
                <option value="onsite">Sur site</option>
              </select>
            </label>
            <label>
              💰 Salaire minimum (€/an)
              <input
                type="number"
                value={salaryMin}
                onChange={(e) => setSalaryMin(Number(e.target.value))}
              />
            </label>
            <label>
              🌍 Pays préférés (codes ISO, séparés par ,)
              <input
                value={preferredCountries}
                onChange={(e) => setPreferredCountries(e.target.value)}
                placeholder="fr, de, us"
              />
            </label>
          </div>

          {/* Affichage données parsées */}
          {profile && profile.skills.length > 0 && (
            <div style={{ marginBottom: 24, padding: 16, background: "rgba(0, 240, 255, 0.1)", borderRadius: 8 }}>
              <p style={{ marginBottom: 8, fontWeight: 600 }}>📊 Données extraites du CV :</p>
              <div>
                <p>Compétences: {profile.skills.join(", ")}</p>
                {profile.experience_years && <p>Expérience: {profile.experience_years} ans</p>}
                {profile.experience_level && <p>Niveau: {profile.experience_level}</p>}
                {profile.languages.length > 0 && <p>Langues: {profile.languages.join(", ")}</p>}
              </div>
            </div>
          )}

          <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
            <button type="submit" disabled={loading} className="btn">
              <span>{loading ? "⏳ Sauvegarde..." : "💾 Sauvegarder le profil"}</span>
            </button>
            {error && <span className="error-text">❌ {error}</span>}
            {success && <span style={{ color: "var(--neon-green)" }}>✅ Profil sauvegardé !</span>}
          </div>
        </form>
      </div>
    </div>
  );
}

