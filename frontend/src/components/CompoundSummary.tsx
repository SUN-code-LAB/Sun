import React from 'react';

export const CompoundSummary = ({ data }: { data: any }) => {
  if (!data) return <div className="p-4 bg-gray-900 rounded-lg border border-gray-800 animate-pulse h-64"></div>;

  const info = data.molecular_info;
  const safety = data.pregnancy_safety;

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
      <h3 className="text-gray-400 text-sm mb-4">Compound Summary</h3>
      <div className="flex justify-between items-end mb-6">
        <div>
          <h2 className="text-3xl font-bold text-white mb-1">Aspirin</h2>
          <p className="text-sm text-gray-400 font-mono">{data.smiles}</p>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
          safety.overall_safety_label === 'Low Risk' ? 'bg-green-900/50 text-green-400 border border-green-800' :
          safety.overall_safety_label === 'Moderate Risk' ? 'bg-yellow-900/50 text-yellow-400 border border-yellow-800' :
          'bg-red-900/50 text-red-400 border border-red-800'
        }`}>
          {safety.overall_safety_label}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-800/50 p-3 rounded-md">
          <p className="text-xs text-gray-500 mb-1">Molecular Weight</p>
          <p className="text-sm font-semibold text-gray-200">{info.mw} g/mol</p>
        </div>
        <div className="bg-gray-800/50 p-3 rounded-md">
          <p className="text-xs text-gray-500 mb-1">Formula</p>
          <p className="text-sm font-semibold text-gray-200">{info.formula}</p>
        </div>
        <div className="bg-gray-800/50 p-3 rounded-md">
          <p className="text-xs text-gray-500 mb-1">LogP</p>
          <p className="text-sm font-semibold text-gray-200">{info.logp}</p>
        </div>
        <div className="bg-gray-800/50 p-3 rounded-md">
          <p className="text-xs text-gray-500 mb-1">TPSA</p>
          <p className="text-sm font-semibold text-gray-200">{info.tpsa}</p>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-gray-800">
        <div className="flex justify-between text-xs">
          <span className="text-gray-500">Analysis Date</span>
          <span className="text-gray-300">23 Aug 2026</span>
        </div>
      </div>
    </div>
  );
};
