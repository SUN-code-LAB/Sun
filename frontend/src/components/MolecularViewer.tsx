import React from 'react';

export const MolecularViewer = () => {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-5 flex flex-col">
      <h3 className="text-gray-400 text-sm mb-4">Molecular Visualization</h3>
      <div className="flex-1 bg-gray-950 rounded-lg border border-gray-800 flex items-center justify-center min-h-[300px] relative overflow-hidden">
        {/* Mock 3D structure visualization using CSS */}
        <div className="absolute inset-0 flex items-center justify-center opacity-30">
          <svg viewBox="0 0 100 100" className="w-full h-full p-10 animate-[spin_60s_linear_infinite]">
            <circle cx="50" cy="50" r="40" stroke="#3b82f6" strokeWidth="1" fill="none" />
            <circle cx="30" cy="30" r="10" fill="#3b82f6" />
            <circle cx="70" cy="70" r="8" fill="#ef4444" />
            <circle cx="70" cy="30" r="6" fill="#ef4444" />
            <line x1="30" y1="30" x2="70" y2="70" stroke="#4b5563" strokeWidth="2" />
            <line x1="30" y1="30" x2="70" y2="30" stroke="#4b5563" strokeWidth="2" />
          </svg>
        </div>
        <div className="z-10 text-center">
          <p className="text-gray-500 text-sm mb-2">3D Conformational View</p>
          <span className="px-3 py-1 bg-gray-800 text-xs text-gray-400 rounded-full border border-gray-700">Interactive Py3Dmol Active</span>
        </div>
      </div>
      <div className="flex gap-2 mt-4">
        <button className="flex-1 py-1.5 bg-blue-600/20 text-blue-400 text-xs rounded border border-blue-600/30 hover:bg-blue-600/30 transition-colors">3D Model</button>
        <button className="flex-1 py-1.5 bg-gray-800 text-gray-400 text-xs rounded border border-gray-700 hover:bg-gray-700 transition-colors">2D Structure</button>
        <button className="flex-1 py-1.5 bg-gray-800 text-gray-400 text-xs rounded border border-gray-700 hover:bg-gray-700 transition-colors">Surface</button>
      </div>
    </div>
  );
};
