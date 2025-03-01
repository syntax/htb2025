import React from 'react';

interface SummaryStats {
  totalValue: number;
  riskLevel: string;
  bestPerformer: string;
  worstPerformer: string;
}

interface PortfolioSummaryProps {
  stats: SummaryStats;
}

const PortfolioSummary: React.FC<PortfolioSummaryProps> = ({ stats }) => {
  return (
    <div className="summary-panel">
      <div className="summary-card">
        <h2>Total Value</h2>
        <p>${stats.totalValue.toLocaleString()}</p>
      </div>
      <div className="summary-card">
        <h2>Risk Level</h2>
        <p>{stats.riskLevel}</p>
      </div>
      <div className="summary-card">
        <h2>Best Performer</h2>
        <p>{stats.bestPerformer}</p>
      </div>
      <div className="summary-card">
        <h2>Worst Performer</h2>
        <p>{stats.worstPerformer}</p>
      </div>
    </div>
  );
};

export default PortfolioSummary;
