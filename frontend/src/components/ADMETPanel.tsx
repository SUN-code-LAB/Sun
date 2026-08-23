import React from 'react';
import { Network, Activity, Milk, AlertTriangle } from 'lucide-react';

export const ADMETPanel = ({ data }: { data: any }) => {
  if (!data) return null;

  return (
    <div className="bg-card border border-card-border rounded-lg p-5">
      <div className="flex items-center gap-2 mb-4">
        <Activity className="text-ai-blue" size={18} />
        <h3 className="font-semibold text-gray-200">ADMET Intelligence</h3>
      </div>

      <div className="space-y-3">
        {Object.entries(data.admet).map(([prop, val]) => (
          <div key={prop} className="flex justify-between items-center bg-gray-900/50 p-2.5 rounded">
            <span className="text-sm text-gray-400">{prop}</span>
            <span className={`text-xs px-2 py-1 rounded-full font-medium ${
              val === 'High' ? (prop === 'Toxicity' ? 'bg-red-900/30 text-risk-red' : 'bg-green-900/30 text-neon-green') :
              val === 'Moderate' ? 'bg-orange-900/30 text-risk-orange' :
              (prop === 'Toxicity' ? 'bg-green-900/30 text-neon-green' : 'bg-red-900/30 text-risk-red')
            }`}>
              {val === 'High' && prop !== 'Toxicity' ? '🟢 High' :
               val === 'Low' && prop === 'Toxicity' ? '🟢 Low' :
               val === 'Moderate' ? '🟡 Moderate' :
               val === 'High' && prop === 'Toxicity' ? '🔴 High' : '🔴 Low'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export const PregnancySafetyPanel = ({ data }: { data: any }) => {
  if (!data) return null;

  return (
    <div className="col-span-1 md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="bg-card border border-card-border rounded-lg p-5">
        <div className="flex items-center gap-2 mb-4">
          <Network className="text-scientific-purple" size={18} />
          <h3 className="font-semibold text-gray-200">Placental Transfer AI</h3>
        </div>
        <div className="flex items-center justify-between mb-4">
          <div className="text-sm text-gray-400">Probability</div>
          <div className="text-xl font-bold text-ai-blue">{Math.round(data.pregnancy_safety.placenta_transfer_prob * 100)}%</div>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-2 mb-4">
          <div className="bg-scientific-purple h-2 rounded-full" style={{ width: `${data.pregnancy_safety.placenta_transfer_prob * 100}%` }}></div>
        </div>
        <div className="bg-gray-900/50 p-3 rounded text-sm">
          <div className="flex justify-between mb-1">
            <span className="text-gray-400">Risk Level</span>
            <span className={`font-semibold ${
              data.pregnancy_safety.placenta_risk === 'High' ? 'text-risk-red' :
              data.pregnancy_safety.placenta_risk === 'Moderate' ? 'text-risk-orange' : 'text-neon-green'
            }`}>{data.pregnancy_safety.placenta_risk}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Mechanism</span>
            <span className="text-gray-300">Passive diffusion likely</span>
          </div>
        </div>
      </div>

      <div className="bg-card border border-card-border rounded-lg p-5">
        <div className="flex items-center gap-2 mb-4">
          <Milk className="text-ai-blue" size={18} />
          <h3 className="font-semibold text-gray-200">Breast Milk Prediction</h3>
        </div>
        <div className="flex items-center justify-between mb-4">
          <div className="text-sm text-gray-400">Probability</div>
          <div className="text-xl font-bold text-ai-blue">{Math.round(data.pregnancy_safety.milk_transfer_prob * 100)}%</div>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-2 mb-4">
          <div className="bg-ai-blue h-2 rounded-full" style={{ width: `${data.pregnancy_safety.milk_transfer_prob * 100}%` }}></div>
        </div>
        <div className="bg-gray-900/50 p-3 rounded text-sm">
          <div className="flex justify-between mb-1">
            <span className="text-gray-400">Milk/Plasma Ratio</span>
            <span className="text-gray-300">{(data.pregnancy_safety.milk_transfer_prob * 1.2).toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Risk Level</span>
            <span className={`font-semibold ${
              data.pregnancy_safety.milk_risk === 'High' ? 'text-risk-red' :
              data.pregnancy_safety.milk_risk === 'Moderate' ? 'text-risk-orange' : 'text-neon-green'
            }`}>{data.pregnancy_safety.milk_risk}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
