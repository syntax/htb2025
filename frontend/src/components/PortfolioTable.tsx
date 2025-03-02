import React from 'react';

interface Data {
  holdings: { [key: string]: number };
  total_ethics: number;
  total_risk: number;
  user_id: number;
}

interface Data2 {
  [key: string]: number;
}

interface PortfolioTableProps {
  data: Data;
  data2: Data2;
  predEod: Data2;
  predEow: Data2;
  predEom: Data2;
}

const PortfolioTable: React.FC<PortfolioTableProps> = ({ 
  data, 
  data2, 
  predEod, 
  predEow, 
  predEom 
}) => {
  if (!data || !data.holdings || !data2) {
    return <div>No data available.</div>;
  }

  const cryptoSymbols = Object.keys(data.holdings);

  return (
    <table className="portfolio-table">
      <thead>
        <tr>
          <th>Crypto</th>
          <th>Portfolio Weights</th>
          <th>Price (USD)</th>
          <th>Total Value (USD)</th>
          <th>Pred EOD Price</th>
          <th>Pred 7 day Price</th>
          <th>Pred 30 day Price</th>
        </tr>
      </thead>
      <tbody>
        {cryptoSymbols.map((symbol) => {
          const balance = data.holdings[symbol];
          const totalValue = data2[symbol] || 0;
          const price = balance ? totalValue / balance : 0;
          const predictionKey = `${symbol}-USD`;

          const eodPrice = predEod[predictionKey];
          const eowPrice = predEow[predictionKey];
          const eomPrice = predEom[predictionKey];

          return (
            <tr key={symbol}>
              <td>{symbol.toUpperCase()}</td>
              <td>{balance.toLocaleString()}</td>
              <td>${price.toFixed(2)}</td>
              <td>${totalValue.toFixed(2)}</td>
              <td>${eodPrice?.toFixed(2) ?? 'N/A'}</td>
              <td>${eowPrice?.toFixed(2) ?? 'N/A'}</td>
              <td>${eomPrice?.toFixed(2) ?? 'N/A'}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default PortfolioTable;