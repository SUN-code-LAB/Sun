import React from 'react';

export const ExplainableAIPanel = () => {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
      <h3 className="text-gray-400 text-sm mb-4">Explainable AI (SHAP)</h3>

      <div className="space-y-4">
        <div>
          <h4 className="text-xs text-red-400 font-semibold mb-2">Risk Increasing Factors</h4>
          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs bg-gray-800/40 p-2 rounded">
              <span className="text-gray-300">↑ LogP (Lipophilicity)</span>
              <span className="text-red-400">+0.35</span>
            </div>
            <div className="flex justify-between items-center text-xs bg-gray-800/40 p-2 rounded">
              <span className="text-gray-300">↓ Molecular weight</span>
              <span className="text-red-400">+0.22</span>
            </div>
            <div className="flex justify-between items-center text-xs bg-gray-800/40 p-2 rounded">
              <span className="text-gray-300">High permeability</span>
              <span className="text-red-400">+0.18</span>
            </div>
          </div>
        </div>

        <div>
          <h4 className="text-xs text-green-400 font-semibold mb-2">Protective Factors</h4>
          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs bg-gray-800/40 p-2 rounded">
              <span className="text-gray-300">Strong protein binding</span>
              <span className="text-green-400">-0.12</span>
            </div>
            <div className="flex justify-between items-center text-xs bg-gray-800/40 p-2 rounded">
              <span className="text-gray-300">↑ TPSA</span>
              <span className="text-green-400">-0.05</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
