/**
 * Home Page Component for Agent Mira Frontend
 * Main landing page with preference form and recommendations
 * Location: client/src/app/page.tsx
 */

"use client";

import { useState, useEffect } from "react";
import { PreferenceForm } from "@/components/forms/PreferenceForm";
import { RecommendationList } from "@/components/recommendations/RecommendationList";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ErrorMessage } from "@/components/ui/ErrorMessage";
import { apiClient, generateSessionId } from "@/lib/api";
import { UserPreferences, Recommendation } from "@/lib/types";

export default function HomePage() {
  // State management
  const [sessionId, setSessionId] = useState<string>("");
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  // Initialize session ID on component mount
  useEffect(() => {
    const savedSessionId = localStorage.getItem("agent_mira_session_id");
    if (savedSessionId) {
      setSessionId(savedSessionId);
    } else {
      const newSessionId = generateSessionId();
      setSessionId(newSessionId);
      localStorage.setItem("agent_mira_session_id", newSessionId);
    }
  }, []);

  // Handle preference form submission
  const handlePreferenceSubmit = async (preferences: UserPreferences) => {
    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      // Submit preferences to backend
      const preferencesResponse = await apiClient.submitPreferences({
        ...preferences,
        session_id: sessionId,
      });

      if (preferencesResponse.error) {
        throw new Error(preferencesResponse.error);
      }

      // Get recommendations
      const recommendationsResponse = await apiClient.getRecommendations(sessionId, 3);

      if (recommendationsResponse.error) {
        throw new Error(recommendationsResponse.error);
      }

      setRecommendations(recommendationsResponse.data || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  // Handle new search
  const handleNewSearch = () => {
    setRecommendations([]);
    setHasSearched(false);
    setError(null);
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Find Your Perfect Home
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-indigo-100">
              AI-powered property recommendations tailored to your preferences
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <div className="flex items-center justify-center space-x-2">
                <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>Smart Matching</span>
              </div>
              <div className="flex items-center justify-center space-x-2">
                <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>ML-Powered</span>
              </div>
              <div className="flex items-center justify-center space-x-2">
                <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>Personalized</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Preference Form */}
            <div className="order-2 lg:order-1">
              <div className="bg-white rounded-lg shadow-lg p-8">
                <div className="mb-6">
                  <h2 className="text-3xl font-bold text-gray-900 mb-2">
                    Tell Us Your Preferences
                  </h2>
                  <p className="text-gray-600">
                    Fill out the form below to get personalized property recommendations
                  </p>
                </div>

                <PreferenceForm
                  onSubmit={handlePreferenceSubmit}
                  loading={loading}
                />
              </div>
            </div>

            {/* Results Section */}
            <div className="order-1 lg:order-2">
              <div className="bg-white rounded-lg shadow-lg p-8">
                <div className="mb-6">
                  <h2 className="text-3xl font-bold text-gray-900 mb-2">
                    Your Recommendations
                  </h2>
                  <p className="text-gray-600">
                    {hasSearched 
                      ? "Here are your personalized property recommendations"
                      : "Submit your preferences to see recommendations"
                    }
                  </p>
                </div>

                {/* Loading State */}
                {loading && (
                  <div className="flex flex-col items-center justify-center py-12">
                    <LoadingSpinner size="lg" />
                    <p className="mt-4 text-gray-600">Finding your perfect matches...</p>
                  </div>
                )}

                {/* Error State */}
                {error && (
                  <ErrorMessage
                    message={error}
                    onRetry={handleNewSearch}
                  />
                )}

                {/* Recommendations */}
                {!loading && !error && recommendations.length > 0 && (
                  <RecommendationList
                    recommendations={recommendations}
                    onNewSearch={handleNewSearch}
                  />
                )}

                {/* Empty State */}
                {!loading && !error && recommendations.length === 0 && hasSearched && (
                  <div className="text-center py-12">
                    <div className="text-gray-400 mb-4">
                      <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-1.009-5.824-2.709" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      No recommendations found
                    </h3>
                    <p className="text-gray-600 mb-4">
                      Try adjusting your preferences to find more properties
                    </p>
                    <button
                      onClick={handleNewSearch}
                      className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
                    >
                      Try Again
                    </button>
                  </div>
                )}

                {/* Initial State */}
                {!loading && !error && !hasSearched && (
                  <div className="text-center py-12">
                    <div className="text-gray-400 mb-4">
                      <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      Ready to find your dream home?
                    </h3>
                    <p className="text-gray-600">
                      Fill out the preference form to get started
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose Agent Mira?
            </h2>
            <p className="text-xl text-gray-600">
              Our AI-powered system provides intelligent property matching
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-indigo-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                AI-Powered Matching
              </h3>
              <p className="text-gray-600">
                Advanced machine learning algorithms analyze your preferences to find the perfect property matches
              </p>
            </div>

            <div className="text-center">
              <div className="bg-indigo-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Lightning Fast
              </h3>
              <p className="text-gray-600">
                Get instant recommendations with our optimized scoring system and real-time processing
              </p>
            </div>

            <div className="text-center">
              <div className="bg-indigo-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Detailed Insights
              </h3>
              <p className="text-gray-600">
                Understand why each property is recommended with detailed scoring breakdowns and reasoning
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}