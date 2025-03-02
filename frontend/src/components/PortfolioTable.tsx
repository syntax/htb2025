import React from 'react';

interface Data {
  holdings: { [key: string]: number };
  total_risk: number;
  total_ethics: number;
  user_id: number;
}

interface Data2 {
  [key: string]: number;
}

interface PortfolioTableProps {
  data: Data;
  data2: Data2;
  pred_eod: { [key: string]: number };
  pred_eow: { [key: string]: number };
  pred_eom: { [key: string]: number };
}

const PortfolioTable: React.FC<PortfolioTableProps> = ({ 
  data, 
  data2, 
  pred_eod, 
  pred_eow, 
  pred_eom 
}) => {
  // Check that the essential data is available.
  if (!data || !data.holdings || !data2) {
    return <div>No data available.</div>;
  }

  // Get the crypto symbols from the holdings object.
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
          // Try to find the total value using the symbol directly or with "-USD" appended.
          const totalValue = 
            data2[symbol] || 
            data2[`${symbol.toUpperCase()}-USD`] || 
            null;
          // If totalValue is available and balance is non-zero, calculate price.
          const price = totalValue !== null && balance 
            ? totalValue / balance 
            : null;

          // Create a prediction key in the format: SYMBOL-USD (e.g., BNB-USD)
          const predictionKey = `${symbol.toUpperCase()}-USD`;
          const eodPrice = pred_eod ? pred_eod[predictionKey] : undefined;
          const eowPrice = pred_eow ? pred_eow[predictionKey] : undefined;
          const eomPrice = pred_eom ? pred_eom[predictionKey] : undefined;

          return (
            <tr key={symbol}>
              <td>{symbol.toUpperCase()}</td>
              <td>{balance.toLocaleString()}</td>
              <td>{price !== null ? `$${price.toFixed(2)}` : 'N/A'}</td>
              <td>{totalValue !== null ? `$${totalValue.toFixed(2)}` : 'N/A'}</td>
              <td>{eodPrice !== undefined ? `$${eodPrice.toFixed(2)}` : 'N/A'}</td>
              <td>{eowPrice !== undefined ? `$${eowPrice.toFixed(2)}` : 'N/A'}</td>
              <td>{eomPrice !== undefined ? `$${eomPrice.toFixed(2)}` : 'N/A'}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default PortfolioTable;
