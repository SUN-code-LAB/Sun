"use client";

import React, { useEffect, useState } from 'react';
import { Navigation } from '@/components/Navigation';
import { Header } from '@/components/Header';
import { CompoundSummary } from '@/components/CompoundSummary';
import { ADMETPanel, MolecularInfoPanel, DrugLikenessPanel } from '@/components/ADMETPanel';
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
    <div className="flex h-screen overflow-hidden bg-navy-950 text-gray-100 font-sans">
      <Navigation />

      <main className="flex-1 flex flex-col h-full overflow-hidden">
        <Header />

        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">

            {/* Top Dashboard */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1">
                <CompoundSummary data={data} />
              </div>

              {/* Middle Dashboard */}
              <div className="lg:col-span-3 grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                  <MolecularViewer />
                </div>
                <div className="space-y-6 flex flex-col h-full">
                  <MolecularInfoPanel data={data} />
                  <DrugLikenessPanel data={data} />
                </div>
              </div>
            </div>

            {/* Bottom Dashboard - Row 1 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data && (
                <div className="bg-navy-900 border border-navy-800 rounded-lg p-5">
                  <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider">CYP450 METABOLISM</h3>
                  <div className="space-y-3">
                    {Object.entries(data.cyp_metabolism).map(([isoform, prediction]) => (
                      <div key={isoform} className="bg-navy-800/40 p-2.5 rounded flex justify-between items-center border border-navy-800/50">
                        <span className="text-sm text-gray-300">{isoform}</span>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-gray-400 w-16 text-right">{prediction as string}</span>
                          <div className={`w-2.5 h-2.5 rounded-full ${
                            prediction === 'High' ? 'bg-red-500' :
                            prediction === 'Moderate' ? 'bg-yellow-500' : 'bg-green-500'
                          }`} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {data && (
                <div className="bg-navy-900 border border-navy-800 rounded-lg p-5">
                  <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider flex items-center gap-2">
                    <span>🫘 RENAL TRANSPORT SYSTEM</span>
                  </h3>
                  <div className="space-y-3">
                    {Object.entries(data.renal_transport).map(([transporter, prob]) => (
                      <div key={transporter} className="bg-navy-800/40 p-2 rounded relative">
                        <div className="flex justify-between items-center mb-1.5">
                          <span className="text-sm font-medium text-gray-300">{transporter}</span>
                          <span className="text-sm text-primary font-mono">{Math.round((prob as number) * 100)}%</span>
                        </div>
                        <div className="w-full bg-navy-950 rounded-full h-1.5 overflow-hidden">
                          <div className="bg-primary h-1.5 rounded-full" style={{ width: `${(prob as number) * 100}%` }}></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {data && (
                <div className="bg-navy-900 border border-navy-800 rounded-lg p-5">
                  <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider flex items-center gap-2">
                    <span>☠ KIDNEY TOXICITY MODULE</span>
                  </h3>
                  <div className="space-y-4">
                    {Object.entries(data.kidney_toxicity).map(([tox, prob]) => (
                      <div key={tox} className="bg-navy-800/40 p-3 rounded">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium text-gray-300">{tox}</span>
                          <span className={`text-sm font-mono ${(prob as number) > 0.7 ? 'text-red-400' : (prob as number) > 0.4 ? 'text-yellow-400' : 'text-green-400'}`}>
                            {Math.round((prob as number) * 100)}%
                          </span>
                        </div>
                        <div className="w-full bg-navy-950 rounded-full h-2 overflow-hidden">
                          <div className={`h-2 rounded-full ${(prob as number) > 0.7 ? 'bg-red-500' : (prob as number) > 0.4 ? 'bg-yellow-500' : 'bg-green-500'}`} style={{ width: `${(prob as number) * 100}%` }}></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Bottom Dashboard - Row 2 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <ADMETPanel data={data} />
              <ExplainableAIPanel />

              {/* History & Quick Actions */}
              <div className="space-y-6">
                <div className="bg-navy-900 border border-navy-800 rounded-lg p-5">
                  <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider">RECENT HISTORY</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center text-xs p-2 bg-navy-800/30 rounded border border-navy-800/50">
                      <span className="text-gray-300">Aspirin</span>
                      <span className="text-green-400">Low Risk</span>
                      <span className="text-gray-500">Today</span>
                    </div>
                    <div className="flex justify-between items-center text-xs p-2 bg-navy-800/30 rounded border border-navy-800/50">
                      <span className="text-gray-300">Cisplatin</span>
                      <span className="text-red-400">High Risk</span>
                      <span className="text-gray-500">Yesterday</span>
                    </div>
                  </div>
                </div>

                <div className="bg-navy-900 border border-navy-800 rounded-lg p-5">
                  <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider">QUICK ACTIONS</h3>
                  <div className="grid grid-cols-2 gap-2">
                    <button className="text-xs py-2 bg-navy-800 hover:bg-primary hover:text-white text-gray-300 rounded transition-colors border border-navy-800 hover:border-primary flex items-center justify-center gap-2">
                      <span>⬆</span> Upload
                    </button>
                    <button className="text-xs py-2 bg-navy-800 hover:bg-primary hover:text-white text-gray-300 rounded transition-colors border border-navy-800 hover:border-primary flex items-center justify-center gap-2">
                      <span>🔍</span> PubChem
                    </button>
                    <button className="text-xs py-2 bg-navy-800 hover:bg-ai hover:text-white text-gray-300 rounded transition-colors border border-navy-800 hover:border-ai flex items-center justify-center gap-2 col-span-2">
                      <span>🧠</span> Train QSAR Model
                    </button>
                    <button className="text-xs py-2 bg-navy-800 hover:bg-primary hover:text-white text-gray-300 rounded transition-colors border border-navy-800 hover:border-primary flex items-center justify-center gap-2 col-span-2">
                      <span>📄</span> Generate Report
                    </button>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
