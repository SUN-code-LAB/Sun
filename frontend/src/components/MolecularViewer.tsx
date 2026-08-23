import React, { useState } from 'react';
import { Maximize2, Download, Rotate3D } from 'lucide-react';

export const MolecularViewer = () => {
  const [view3D, setView3D] = useState(false);

  return (
    <div className="bg-card border border-card-border rounded-lg h-full flex flex-col">
      <div className="p-4 border-b border-card-border flex justify-between items-center">
        <h3 className="font-semibold text-white">Molecular Structure</h3>
        <div className="flex bg-gray-900 rounded-lg p-1">
          <button
            className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${!view3D ? 'bg-card border border-card-border text-ai-blue' : 'text-gray-400 hover:text-gray-200'}`}
            onClick={() => setView3D(false)}
          >
            2D
          </button>
          <button
            className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${view3D ? 'bg-card border border-card-border text-scientific-purple' : 'text-gray-400 hover:text-gray-200'}`}
            onClick={() => setView3D(true)}
          >
            3D
          </button>
        </div>
      </div>

      <div className="flex-1 relative bg-gray-950 m-4 rounded-lg flex items-center justify-center border border-gray-800 overflow-hidden">
        {/* Placeholder for actual RDKit / Py3Dmol rendering */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-500">
          {view3D ? (
            <>
              <Rotate3D size={48} className="text-gray-700 mb-4 animate-spin-slow" />
              <p className="text-sm">Py3Dmol Canvas Placeholder</p>
              <p className="text-xs text-gray-600 mt-2">Interactive 3D rendering</p>
            </>
          ) : (
            <>
              <div className="w-48 h-48 border-2 border-dashed border-gray-700 rounded-full flex items-center justify-center mb-4">
                <span className="text-gray-600 text-xs">RDKit SVG</span>
              </div>
              <p className="text-sm">2D Structure Placeholder</p>
            </>
          )}
        </div>

        <div className="absolute top-2 right-2 flex gap-2">
          <button className="p-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded transition-colors" title="Download">
            <Download size={16} />
          </button>
          <button className="p-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded transition-colors" title="Fullscreen">
            <Maximize2 size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};
