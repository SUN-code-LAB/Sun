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
    <div className="flex h-screen overflow-hidden bg-gray-950 text-gray-100 font-sans">
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
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
                  <h3 className="text-gray-400 text-sm mb-4">Drug Metabolism (CYP450)</h3>
                  <div className="grid grid-cols-2 gap-3">
                    {Object.entries(data.cyp_metabolism).map(([isoform, prediction]) => (
                      <div key={isoform} className="bg-gray-800/40 p-3 rounded flex justify-between items-center">
                        <span className="text-sm font-medium text-gray-300">{isoform}</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${
                          prediction === 'High' ? 'bg-red-900/50 text-red-400' :
                          prediction === 'Moderate' ? 'bg-yellow-900/50 text-yellow-400' :
                          'bg-green-900/50 text-green-400'
                        }`}>
                          {prediction as string}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
                  <h3 className="text-gray-400 text-sm mb-4">Placental Transport System</h3>
                  <div className="space-y-3">
                    {Object.entries(data.placental_transport).map(([transporter, prob]) => (
                      <div key={transporter} className="bg-gray-800/40 p-3 rounded">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium text-gray-300">{transporter}</span>
                          <span className="text-sm text-blue-400 font-semibold">{Math.round((prob as number) * 100)}%</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-1.5">
                          <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: `${(prob as number) * 100}%` }}></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

          </div>
        </div>
      </main>
    </div>
  );
}
