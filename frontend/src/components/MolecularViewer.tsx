import React from 'react';

export const MolecularViewer = () => {
  return (
    <div className="bg-navy-900 border border-navy-800 rounded-lg p-5 flex flex-col h-full">
      <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider flex justify-between">
        <span>MOLECULAR STRUCTURE</span>
      </h3>
      <div className="flex-1 flex gap-4 min-h-[300px]">
        {/* 2D Structure (Left) */}
        <div className="flex-1 bg-navy-950 rounded-lg border border-navy-800 flex flex-col items-center justify-center relative overflow-hidden">
          <div className="absolute top-2 left-2 px-2 py-1 bg-navy-800 text-[10px] text-gray-400 rounded-sm">RDKit 2D</div>
          {/* Mock 2D Hexagon */}
          <svg width="120" height="120" viewBox="0 0 100 100" className="opacity-80">
            <polygon points="50,10 90,30 90,70 50,90 10,70 10,30" fill="none" stroke="#00A8FF" strokeWidth="2" />
            <line x1="50" y1="15" x2="85" y2="33" stroke="#00A8FF" strokeWidth="1" />
            <line x1="15" y1="33" x2="15" y2="67" stroke="#00A8FF" strokeWidth="1" />
            <line x1="50" y1="85" x2="85" y2="67" stroke="#00A8FF" strokeWidth="1" />
          </svg>
        </div>

        {/* 3D Structure (Right) */}
        <div className="flex-[1.5] bg-navy-950 rounded-lg border border-navy-800 flex flex-col relative overflow-hidden">
          <div className="absolute top-2 left-2 px-2 py-1 bg-navy-800 text-[10px] text-gray-400 rounded-sm z-10">Py3Dmol</div>

          <div className="absolute inset-0 flex items-center justify-center opacity-40">
            <svg viewBox="0 0 100 100" className="w-full h-full p-10 animate-[spin_60s_linear_infinite]">
              <circle cx="50" cy="50" r="40" stroke="#8A2BE2" strokeWidth="1" fill="none" />
              <circle cx="30" cy="30" r="10" fill="#00A8FF" />
              <circle cx="70" cy="70" r="8" fill="#ef4444" />
              <circle cx="70" cy="30" r="6" fill="#ef4444" />
              <line x1="30" y1="30" x2="70" y2="70" stroke="#132145" strokeWidth="2" />
              <line x1="30" y1="30" x2="70" y2="30" stroke="#132145" strokeWidth="2" />
            </svg>
          </div>

          {/* Controls Overlay */}
          <div className="absolute bottom-3 right-3 flex gap-2 z-10">
            <button className="p-1.5 bg-navy-800 text-gray-300 text-xs rounded hover:bg-primary hover:text-white transition-colors" title="Rotate">🔄</button>
            <button className="p-1.5 bg-navy-800 text-gray-300 text-xs rounded hover:bg-primary hover:text-white transition-colors" title="Zoom">🔍</button>
            <button className="p-1.5 bg-navy-800 text-gray-300 text-xs rounded hover:bg-primary hover:text-white transition-colors" title="Ball & Stick">⚪</button>
            <button className="p-1.5 bg-navy-800 text-gray-300 text-xs rounded hover:bg-primary hover:text-white transition-colors" title="Surface View">🌐</button>
            <button className="p-1.5 bg-navy-800 text-gray-300 text-xs rounded hover:bg-primary hover:text-white transition-colors" title="Download">⬇</button>
          </div>
        </div>
      </div>
    </div>
  );
};
