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
}

const PortfolioTable: React.FC<PortfolioTableProps> = ({ data, data2 }) => {
  // Get an array of crypto symbols from the holdings object
  
  if (!data || !data.holdings || !data2) {
    return <div>No data available.</div>;
  }
  const cryptoSymbols = Object.keys(data.holdings);
  

  return (
    <table className="portfolio-table">
      <thead>
        <tr>
          <th>Crypto</th>
          <th>Balance</th>
          <th>Price (USD)</th>
          <th>Total Value (USD)</th>
        </tr>
      </thead>
      <tbody>
        {cryptoSymbols.map((symbol) => {
          const balance = data.holdings[symbol];
          // Retrieve the total value for this crypto from data2, defaulting to 0 if not found
          const totalValue = data2[symbol] || 0;
          // Calculate the price per coin (guarding against division by zero)
          const price = balance ? totalValue / balance : 0;

          return (
            <tr key={symbol}>
              <td>{symbol.toUpperCase()}</td>
              <td>{balance}</td>
              <td>${price.toLocaleString()}</td>
              <td>${totalValue.toLocaleString()}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default PortfolioTable;
