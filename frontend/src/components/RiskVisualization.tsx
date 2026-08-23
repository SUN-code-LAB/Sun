import React from 'react';
import { BrainCircuit, TrendingUp, TrendingDown } from 'lucide-react';

export const ExplainableAIPanel = () => {
  return (
    <div className="bg-card border border-card-border rounded-lg p-5">
      <div className="flex items-center gap-2 mb-4">
        <BrainCircuit className="text-ai-blue" size={18} />
        <h3 className="font-semibold text-gray-200">Explainable AI (SHAP)</h3>
      </div>

      <p className="text-xs text-gray-400 mb-4">Why did the AI predict this?</p>

      <div className="space-y-4">
        <div>
          <div className="text-xs font-semibold text-risk-red mb-2 flex items-center gap-1">
            <TrendingUp size={14} /> Risk Increasing Features
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-300">LogP</span>
              <span className="text-risk-red font-mono">+0.35</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-1.5">
              <div className="bg-risk-red h-1.5 rounded-full" style={{ width: '70%' }}></div>
            </div>

            <div className="flex justify-between items-center text-sm pt-1">
              <span className="text-gray-300">Low Molecular Wt</span>
              <span className="text-risk-red font-mono">+0.22</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-1.5">
              <div className="bg-risk-red h-1.5 rounded-full" style={{ width: '45%' }}></div>
            </div>

            <div className="flex justify-between items-center text-sm pt-1">
              <span className="text-gray-300">High Permeability</span>
              <span className="text-risk-red font-mono">+0.18</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-1.5">
              <div className="bg-risk-red h-1.5 rounded-full" style={{ width: '35%' }}></div>
            </div>
          </div>
        </div>

        <div className="pt-2 border-t border-gray-800">
          <div className="text-xs font-semibold text-neon-green mb-2 flex items-center gap-1">
            <TrendingDown size={14} /> Risk Reducing Features
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-300">Protein Binding</span>
              <span className="text-neon-green font-mono">-0.12</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-1.5 flex justify-end">
              <div className="bg-neon-green h-1.5 rounded-full" style={{ width: '25%' }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
