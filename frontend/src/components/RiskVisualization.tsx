import React from 'react';

export const ExplainableAIPanel = () => {
  return (
    <div className="bg-navy-900 border border-navy-800 rounded-lg p-5">
      <h3 className="text-primary text-sm mb-4 font-semibold tracking-wider">EXPLAINABLE AI (SHAP)</h3>

      <div className="space-y-4">
        <div>
          <h4 className="text-xs text-red-400 font-semibold mb-2">Feature Contribution</h4>
          <div className="space-y-2 relative">
            <div className="flex justify-between items-center text-xs bg-navy-800/40 p-2 rounded relative overflow-hidden">
              <div className="absolute top-0 left-0 bottom-0 bg-red-900/30 w-[85%] z-0 border-l-2 border-red-500"></div>
              <span className="text-gray-300 z-10">LogP</span>
              <span className="text-red-400 font-mono z-10">+35%</span>
            </div>
            <div className="flex justify-between items-center text-xs bg-navy-800/40 p-2 rounded relative overflow-hidden">
              <div className="absolute top-0 left-0 bottom-0 bg-red-900/30 w-[70%] z-0 border-l-2 border-red-500"></div>
              <span className="text-gray-300 z-10">Solubility</span>
              <span className="text-red-400 font-mono z-10">+30%</span>
            </div>
            <div className="flex justify-between items-center text-xs bg-navy-800/40 p-2 rounded relative overflow-hidden">
              <div className="absolute top-0 left-0 bottom-0 bg-red-900/30 w-[45%] z-0 border-l-2 border-red-500"></div>
              <span className="text-gray-300 z-10">Molecular Weight</span>
              <span className="text-red-400 font-mono z-10">+20%</span>
            </div>
            <div className="flex justify-between items-center text-xs bg-navy-800/40 p-2 rounded relative overflow-hidden">
              <div className="absolute top-0 left-0 bottom-0 bg-red-900/30 w-[35%] z-0 border-l-2 border-red-500"></div>
              <span className="text-gray-300 z-10">TPSA</span>
              <span className="text-red-400 font-mono z-10">+15%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
