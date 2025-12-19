"use client";

import { FormEvent, useState } from "react";

type JobPosting = {
  id: string;
  title: string;
  company?: string;
  country?: string;
  city?: string;
  remote_type?: string;
  contract_type?: string;
  salary_min?: number;
  salary_max?: number;
  currency?: string;
  salary_period?: string;
  apply_url?: string;
  match_score?: number;
  reasons?: string[];
  skills?: string[];
};

type SearchResponse = {
  total: number;
  items: JobPosting[];
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";


const IT_CATEGORIES = [
  "Frontend Dev",
  "Backend Dev",
  "Fullstack Dev",
  "Mobile Dev",
  "DevOps/SRE",
  "Cloud Architect",
  "Data Engineer",
  "Data Scientist",
  "ML Engineer",
  "AI Researcher",
  "QA/Test Engineer",
  "Security Engineer",
  "Blockchain Dev",
  "Game Dev",
  "Embedded/IoT",
  "Tech Lead",
  "Engineering Manager",
  "Product Manager",
  "UI/UX Designer",
  "Solutions Architect",
];

export default function Page() {
  const [keywords, setKeywords] = useState("python fastapi");
  const [selectedCategories, setSelectedCategories] = useState<string[]>(["Backend Dev"]);
  const [countries, setCountries] = useState("fr");
  const [contract, setContract] = useState("CDI");
  const [remote, setRemote] = useState("hybrid");
  const [salary, setSalary] = useState(45000);
  const [cvSummary, setCvSummary] = useState("5 ans backend python fastapi postgres");
  const [loading, setLoading] = useState(false);
  const [offers, setOffers] = useState<JobPosting[]>([]);
  const [error, setError] = useState<string | null>(null);

  const toggleCategory = (cat: string) => {
    setSelectedCategories((prev) =>
      prev.includes(cat) ? prev.filter((c) => c !== cat) : [...prev, cat]
    );
  };

  async function runSearch(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const requestBody = {
        keywords: [...keywords.split(" ").filter(Boolean), ...selectedCategories],
        countries: countries.split(",").map((c) => c.trim()).filter(Boolean),
        contract_types: contract ? [contract] : [],
        remote_preference: remote || null,
        salary_min: salary || null,
        cv_summary: cvSummary || null,
      };

      // 1) ingest
      await fetch(`${API_BASE}/ingest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });
      // 2) search
      const res = await fetch(`${API_BASE}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });
      if (!res.ok) throw new Error(`API ${res.status}`);
      const data: SearchResponse = await res.json();
      setOffers(data.items);
    } catch (err: any) {
      setError(err.message || "Erreur réseau");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <h1>⚡ DevJobs Hunter ⚡</h1>
      <p className="subtitle">
        🚀 Moteur de recherche d&apos;emploi cyberpunk pour les devs · API: {API_BASE}
      </p>

      <form className="card search-form" onSubmit={runSearch}>
        <div style={{ marginBottom: 24 }}>
          <label>🎯 Catégories IT</label>
          <div className="category-select">
            {IT_CATEGORIES.map((cat) => (
              <button
                key={cat}
                type="button"
                className={`category-btn ${selectedCategories.includes(cat) ? "active" : ""}`}
                onClick={() => toggleCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        <div className="grid">
          <label>
            🔍 Mots-clés tech
            <input
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              placeholder="python, react, kubernetes..."
            />
          </label>
          <label>
            🌍 Pays (codes ISO)
            <input
              value={countries}
              onChange={(e) => setCountries(e.target.value)}
              placeholder="fr, de, us..."
            />
          </label>
          <label>
            📝 Type de contrat
            <select value={contract} onChange={(e) => setContract(e.target.value)}>
              <option value="CDI">CDI</option>
              <option value="CDD">CDD</option>
              <option value="Freelance">Freelance</option>
              <option value="Internship">Stage</option>
              <option value="">Tous</option>
            </select>
          </label>
          <label>
            🏠 Remote
            <select value={remote} onChange={(e) => setRemote(e.target.value)}>
              <option value="remote">Full remote</option>
              <option value="hybrid">Hybride</option>
              <option value="onsite">Sur site</option>
              <option value="">Tous</option>
            </select>
          </label>
          <label>
            💰 Salaire minimum (€/an)
            <input
              type="number"
              value={salary}
              onChange={(e) => setSalary(Number(e.target.value))}
              placeholder="45000"
            />
          </label>
          <label>
            📄 Résumé CV / Profil
            <textarea
              value={cvSummary}
              onChange={(e) => setCvSummary(e.target.value)}
              placeholder="Ex: 5 ans backend Python/Go, expert Kubernetes, IA..."
              rows={3}
            />
          </label>
        </div>

        <div style={{ marginTop: 24, display: "flex", gap: 16, alignItems: "center" }}>
          <button type="submit" disabled={loading} className="btn">
            <span>{loading ? "⏳ SCAN EN COURS..." : "🚀 LANCER SCAN"}</span>
          </button>
          {error && <span className="error-text">❌ {error}</span>}
        </div>
      </form>

      <div style={{ marginTop: 16, marginBottom: 8, opacity: 0.7 }}>
        {offers.length > 0 && (
          <p style={{ fontFamily: "Orbitron, sans-serif", fontSize: "0.9rem", letterSpacing: 1 }}>
            ⚡ {offers.length} OFFRE{offers.length > 1 ? "S" : ""} TROUVÉE{offers.length > 1 ? "S" : ""}
          </p>
        )}
      </div>

      {offers.map((job) => (
        <div key={job.id} className="card job-card">
          <div className="job-header">
            <div>
              <h3 className="job-title">{job.title}</h3>
              <p className="job-company">
                🏢 {job.company || "Entreprise"} · 📍 {job.city || "N/A"}, {job.country || "N/A"}
              </p>
            </div>
            <div className="job-badges">
              <span className="badge score">⚡ {job.match_score ?? 0}</span>
              {job.remote_type && <span className="badge">🏠 {job.remote_type}</span>}
              {job.contract_type && <span className="badge">📝 {job.contract_type}</span>}
            </div>
          </div>

          <p style={{ marginTop: 8, color: "#c5d4ff" }}>
            💰{" "}
            {job.salary_min
              ? `${job.salary_min}-${job.salary_max ?? ""} ${job.currency ?? "EUR"} / ${
                  job.salary_period ?? "year"
                }`
              : "Salaire non communiqué"}
          </p>

          {job.skills && job.skills.length > 0 && (
            <div style={{ marginTop: 12 }}>
              {job.skills.map((s) => (
                <span key={s} className="badge">
                  {s}
                </span>
              ))}
            </div>
          )}

          {job.reasons && job.reasons.length > 0 && (
            <p style={{ marginTop: 12, color: "#9fb3d8", fontSize: "0.9rem" }}>
              💡 {job.reasons.join(" · ")}
            </p>
          )}

          {job.apply_url && (
            <div style={{ marginTop: 16 }}>
              <a href={job.apply_url} target="_blank" rel="noreferrer">
                🚀 POSTULER
              </a>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
