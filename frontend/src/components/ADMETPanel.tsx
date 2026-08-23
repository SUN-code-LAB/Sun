import React from 'react';

const StatusDot = ({ status }: { status: string }) => {
  const colorClass = status === 'High' ? 'bg-red-500' : status === 'Moderate' ? 'bg-yellow-500' : 'bg-green-500';
  return <div className={`w-2.5 h-2.5 rounded-full ${colorClass}`} />;
};

export const ADMETPanel = ({ data }: { data: any }) => {
  if (!data) return <div className="p-4 bg-gray-900 rounded-lg border border-gray-800 animate-pulse h-64"></div>;

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
      <h3 className="text-gray-400 text-sm mb-4">ADMET Intelligence</h3>

      <div className="space-y-3">
        {Object.entries(data.admet).map(([key, value]) => (
          <div key={key} className="flex items-center justify-between bg-gray-800/30 p-2.5 rounded border border-gray-800/50">
            <span className="text-sm text-gray-300">{key}</span>
            <div className="flex items-center gap-2">
              <StatusDot status={value as string} />
              <span className="text-xs text-gray-400 w-16 text-right">{value as string}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export const PregnancySafetyPanel = ({ data }: { data: any }) => {
  if (!data) return <div className="p-4 bg-gray-900 rounded-lg border border-gray-800 animate-pulse h-64"></div>;

  const safety = data.pregnancy_safety;

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
      <h3 className="text-gray-400 text-sm mb-4">Pregnancy Safety Prediction</h3>

      <div className="space-y-4">
        <div>
          <div className="flex justify-between mb-1">
            <span className="text-sm text-gray-300">Placental Transfer</span>
            <span className="text-sm font-semibold text-blue-400">{Math.round(safety.placenta_transfer_prob * 100)}%</span>
          </div>
          <div className="w-full bg-gray-800 rounded-full h-2">
            <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${safety.placenta_transfer_prob * 100}%` }}></div>
          </div>
        </div>

        <div>
          <div className="flex justify-between mb-1">
            <span className="text-sm text-gray-300">Breast Milk Transfer</span>
            <span className="text-sm font-semibold text-purple-400">{Math.round(safety.milk_transfer_prob * 100)}%</span>
          </div>
          <div className="w-full bg-gray-800 rounded-full h-2">
            <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${safety.milk_transfer_prob * 100}%` }}></div>
          </div>
        </div>

        <div className="pt-3 border-t border-gray-800 grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs text-gray-500 mb-1">Fetal Exposure Risk</p>
            <p className="text-sm font-semibold text-gray-200">{safety.placenta_risk}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">Developmental Tox</p>
            <p className="text-sm font-semibold text-gray-200">{safety.toxicity_risk}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
