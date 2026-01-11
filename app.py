
import React, { useState, useEffect } from 'react';
import { getKnowledgeBankData } from '../services/mockData';
import type { JobProfileAnalysis } from '../types';
import { RadarChart } from './RadarChart';

export const KnowledgeBank: React.FC = () => {
  const [profiles, setProfiles] = useState<JobProfileAnalysis[]>([]);
  const [selectedProfileId, setSelectedProfileId] = useState<string>('');

  useEffect(() => {
    const data = getKnowledgeBankData();
    setProfiles(data);
    if (data.length > 0) {
      setSelectedProfileId(data[0].id);
    }
  }, []);

  const selectedProfile = profiles.find(p => p.id === selectedProfileId);

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-3xl font-bold text-bp-text mb-4 sm:mb-0">Vidensbank</h1>
        {profiles.length > 0 && (
          <select
            value={selectedProfileId}
            onChange={(e) => setSelectedProfileId(e.target.value)}
            className="w-full sm:w-72 bg-bp-bg-light border border-bp-accent/50 text-bp-text rounded-md px-3 py-2 focus:ring-2 focus:ring-bp-accent focus:outline-none"
            aria-label="Vælg jobprofil"
          >
            {profiles.map(profile => (
              <option key={profile.id} value={profile.id}>
                {profile.title}
              </option>
            ))}
          </select>
        )}
      </div>

      {selectedProfile ? (
        <div className="grid grid-cols-1 gap-8">
          {/* Employer Attractiveness */}
          <div className="bg-bp-bg-light p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold text-bp-text mb-4">Employer Attraktivitet</h2>
            <p className="text-bp-text-secondary mb-6">
              En analyse af jeres tiltrækningskraft på kandidatmarkedet for rollen som {selectedProfile.title}, baseret på benchmark data og kandidatfeedback.
            </p>
            <div className="flex justify-center items-center">
              <RadarChart data={selectedProfile.attractiveness} />
            </div>
          </div>

          {/* Recommended Actions */}
          <div className="bg-bp-bg-light p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold text-bp-text mb-4">Anbefalede Handlinger</h2>
            <p className="text-bp-text-secondary mb-6">
              Baseret på analysen er her de mest effektive tiltag for at styrke jeres position.
            </p>
            <ul className="space-y-6">
              {selectedProfile.recommendations.map((rec, index) => (
                <li key={index} className="flex">
                   <div className="flex-shrink-0">
                    <div className="flex items-center justify-center h-10 w-10 rounded-full bg-bp-accent/20 text-bp-accent">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-bp-text">{rec.title}</h3>
                    <p className="mt-1 text-bp-text-secondary">{rec.description}</p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      ) : (
        <p className="text-bp-text-secondary">Indlæser data...</p>
      )}
    </div>
  );
};
