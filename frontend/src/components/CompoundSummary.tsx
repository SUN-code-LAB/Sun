import React from 'react';

export const CompoundSummary = ({ data }: { data: any }) => {
  if (!data) return <div className="p-4 bg-navy-900 rounded-lg border border-navy-800 animate-pulse h-64"></div>;

  const info = data.molecular_info;

  return (
    <div className="bg-navy-900 border border-navy-800 rounded-lg p-5 glassmorphism">
      <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider">COMPOUND</h3>

      <div className="flex flex-col mb-6 space-y-1 border-b border-navy-800 pb-4">
        <h2 className="text-3xl font-bold text-white tracking-wide">{data.compound || 'Aspirin'}</h2>
        <p className="text-sm text-gray-400 font-mono mb-2">PubChem CID: 2244</p>
      </div>

      <div className="space-y-4">
        <div>
          <p className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Molecular Weight</p>
          <p className="text-lg font-semibold text-gray-200">{info.mw} g/mol</p>
        </div>

        <div>
          <p className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Formula</p>
          <p className="text-lg font-semibold text-gray-200">{info.formula}</p>
        </div>

        <div>
          <p className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Analysis Date</p>
          <p className="text-lg font-semibold text-gray-200">23 Aug 2026</p>
        </div>

        <div>
          <p className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Overall Risk</p>
          <p className={`text-lg font-semibold ${
            data.overall_safety_label.includes('Low') ? 'text-green-400' :
            data.overall_safety_label.includes('Moderate') ? 'text-yellow-400' : 'text-red-400'
          }`}>
            {data.overall_safety_label}
          </p>
        </div>
      </div>
    </div>
  );
};
