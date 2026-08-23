import React from 'react';
import { Activity, ShieldCheck, ShieldAlert, Check } from 'lucide-react';

export const CompoundSummary = ({ data }: { data: any }) => {
  if (!data) return (
    <div className="bg-card border border-card-border rounded-lg p-6 animate-pulse">
      <div className="h-6 bg-gray-800 rounded w-1/4 mb-4"></div>
      <div className="h-32 bg-gray-800 rounded mb-4"></div>
    </div>
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Summary Module */}
      <div className="bg-card border border-card-border rounded-lg p-6">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold text-white">{data.compound}</h2>
            <p className="text-sm text-ai-blue font-mono mt-1">{data.smiles}</p>
          </div>
          <div className="px-3 py-1 rounded bg-ai-blue/10 border border-ai-blue/30 text-ai-blue text-sm font-medium">
            Compound Summary
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-900/50 p-4 rounded-lg">
            <span className="text-gray-400 text-xs block mb-1">Molecular Weight</span>
            <span className="text-lg font-semibold text-gray-200">{data.molecular_info?.mw || '---'}</span>
          </div>
          <div className="bg-gray-900/50 p-4 rounded-lg">
            <span className="text-gray-400 text-xs block mb-1">Formula</span>
            <span className="text-lg font-semibold text-gray-200">{data.molecular_info?.formula || '---'}</span>
          </div>
          <div className="bg-gray-900/50 p-4 rounded-lg">
            <span className="text-gray-400 text-xs block mb-1">Overall Risk</span>
            <span className={`text-lg font-semibold ${
              data.pregnancy_safety?.overall_safety_label === 'High Risk' ? 'text-risk-red' :
              data.pregnancy_safety?.overall_safety_label === 'Moderate Risk' ? 'text-risk-orange' :
              'text-neon-green'
            }`}>
              {data.pregnancy_safety?.overall_safety_label || '---'}
            </span>
          </div>
          <div className="bg-gray-900/50 p-4 rounded-lg">
            <span className="text-gray-400 text-xs block mb-1">LogP</span>
            <span className="text-lg font-semibold text-gray-200">{data.molecular_info?.logp || '---'}</span>
          </div>
        </div>
      </div>

      {/* Molecular Info & Drug-Likeness Module */}
      <div className="bg-card border border-card-border rounded-lg p-6">
        <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
          <Activity size={16} className="text-scientific-purple" />
          Molecular Information
        </h3>

        <div className="grid grid-cols-2 gap-x-4 gap-y-2 mb-6">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Atoms</span>
            <span className="text-gray-200">{data.molecular_info?.atoms}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Bonds</span>
            <span className="text-gray-200">{data.molecular_info?.bonds}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">TPSA</span>
            <span className="text-gray-200">{data.molecular_info?.tpsa}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">HBD</span>
            <span className="text-gray-200">{data.molecular_info?.hbd}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">HBA</span>
            <span className="text-gray-200">{data.molecular_info?.hba}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Rotatable Bonds</span>
            <span className="text-gray-200">{data.molecular_info?.rotatable_bonds}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Aromatic Rings</span>
            <span className="text-gray-200">{data.molecular_info?.aromatic_rings}</span>
          </div>
        </div>

        <div className="border-t border-card-border pt-4">
          <h4 className="text-xs font-semibold text-gray-400 mb-3 uppercase tracking-wider">Drug Likeness (Lipinski)</h4>
          <div className="grid grid-cols-2 gap-2 text-sm text-gray-300">
            <div className="flex items-center gap-2">
              <Check size={14} className="text-neon-green" /> MW &lt;500
            </div>
            <div className="flex items-center gap-2">
              <Check size={14} className="text-neon-green" /> LogP &lt;5
            </div>
            <div className="flex items-center gap-2">
              <Check size={14} className="text-neon-green" /> HBD &lt;5
            </div>
            <div className="flex items-center gap-2">
              <Check size={14} className="text-neon-green" /> HBA &lt;10
            </div>
          </div>
          <div className="mt-4 flex items-center justify-between bg-gray-900/50 p-3 rounded">
            <span className="text-sm font-medium text-gray-400">Result</span>
            <span className={`text-sm font-bold flex items-center gap-2 ${data.molecular_info?.drug_likeness === 'Yes' ? 'text-neon-green' : 'text-risk-red'}`}>
              {data.molecular_info?.drug_likeness === 'Yes' ? <ShieldCheck size={16} /> : <ShieldAlert size={16} />}
              {data.molecular_info?.drug_likeness === 'Yes' ? 'Drug-like' : 'Not Drug-like'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
