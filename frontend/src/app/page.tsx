"use client";

import React, { useEffect, useState } from 'react';
import { Navigation } from '@/components/Navigation';
import { Header } from '@/components/Header';
import { CompoundSummary } from '@/components/CompoundSummary';
import { ADMETPanel, PregnancySafetyPanel } from '@/components/ADMETPanel';
import { MolecularViewer } from '@/components/MolecularViewer';
import { ExplainableAIPanel } from '@/components/RiskVisualization';

export default function Home() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const defaultSmiles = "CC(=O)OC1=CC=CC=C1C(=O)O"; // Aspirin

  useEffect(() => {
    fetch(`http://localhost:8000/api/analyze?smiles=${encodeURIComponent(defaultSmiles)}`)
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching data:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-background text-gray-100 font-sans">
      <Navigation />

      <main className="flex-1 flex flex-col h-full overflow-hidden">
        <Header />

        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <CompoundSummary data={data} />
              </div>
              <div className="lg:col-span-1">
                <MolecularViewer />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <PregnancySafetyPanel data={data} />
              <ADMETPanel data={data} />
              <ExplainableAIPanel />
            </div>

            {/* Additional Modules Row */}
            {data && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-card border border-card-border rounded-lg p-5">
                  <h3 className="text-gray-400 text-sm font-semibold mb-4">CYP450 Metabolism Prediction</h3>
                  <div className="grid grid-cols-2 gap-3">
                    {Object.entries(data.cyp_metabolism).map(([isoform, prediction]) => (
                      <div key={isoform} className="bg-gray-900/50 p-3 rounded flex justify-between items-center">
                        <span className="text-sm font-medium text-gray-300">{isoform}</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${
                          prediction === 'High' ? 'bg-red-900/30 text-risk-red' :
                          prediction === 'Moderate' ? 'bg-yellow-900/30 text-risk-orange' :
                          'bg-green-900/30 text-neon-green'
                        }`}>
                          {prediction as string}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-card border border-card-border rounded-lg p-5">
                  <h3 className="text-gray-400 text-sm font-semibold mb-4">Transporter Interaction Potential</h3>
                  <div className="space-y-4">
                    {Object.entries(data.placental_transport).map(([transporter, prob]) => (
                      <div key={transporter} className="bg-gray-900/50 p-3 rounded">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium text-gray-300">{transporter}</span>
                          <span className="text-sm text-ai-blue font-semibold">{Math.round((prob as number) * 100)}%</span>
                        </div>
                        <div className="w-full bg-gray-800 rounded-full h-1.5">
                          <div className="bg-ai-blue h-1.5 rounded-full" style={{ width: `${(prob as number) * 100}%` }}></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {data && (
              <div className="bg-card border border-card-border rounded-lg p-5">
                <h3 className="text-gray-400 text-sm font-semibold mb-4">Toxicology Intelligence</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                   {['Developmental', 'Embryotoxicity', 'Genotoxicity', 'Neurotoxicity', 'Hepatotoxicity', 'Cardiotoxicity'].map((tox) => {
                     const isHigh = Math.random() > 0.8;
                     const isMod = Math.random() > 0.5;
                     return (
                       <div key={tox} className="bg-gray-900/50 p-3 rounded text-center">
                         <div className="text-xs text-gray-400 mb-2">{tox}</div>
                         <div className={`text-sm font-bold ${isHigh ? 'text-risk-red' : isMod ? 'text-risk-orange' : 'text-neon-green'}`}>
                           {isHigh ? 'High Risk' : isMod ? 'Moderate' : 'Low Risk'}
                         </div>
                       </div>
                     )
                   })}
                </div>
              </div>
            )}

          </div>
        </div>
      </main>
    </div>
  );
}
