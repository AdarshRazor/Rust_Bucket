'use client'

import Image from "next/image";
import UserPreferenceForm from "../components/UserPreferenceForm";
import ResultsDisplay from "../components/ResultsDisplay";
import React, { useState } from "react";

export default function Home() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(form: any) {
    setLoading(true);
    setError("");
    setRecommendations([]);
    try {
      const res = await fetch("http://localhost:8000/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("Failed to fetch recommendations");
      const data = await res.json();
      setRecommendations(data.recommendations || []);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="font-sans min-h-screen p-8 pb-20 flex flex-col items-center gap-8 bg-blue-50">
      <header className="mb-4 flex flex-col items-center">
        <h1 className="text-3xl font-extrabold text-blue-900 mt-2 mb-1">Agent Mira: Property Recommendations</h1>
        <p className="text-blue-700 text-lg font-medium">Find your perfect home, powered by AI</p>
      </header>
      <UserPreferenceForm onSubmit={handleSubmit} />
      {loading && <div className="text-blue-600">Loading recommendations...</div>}
      {error && <div className="text-red-600">{error}</div>}
      <ResultsDisplay recommendations={recommendations} />
    </div>
  );
}
