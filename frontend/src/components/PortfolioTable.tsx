import React from 'react';
import { CryptoCoin } from '../App';

interface PortfolioTableProps {
  portfolio: CryptoCoin[];
}

const PortfolioTable: React.FC<PortfolioTableProps> = ({ portfolio }) => {
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
        {portfolio.map((coin) => (
          <tr key={coin.id}>
            <td>
              {coin.name} <span className="symbol">({coin.symbol})</span>
            </td>
            <td>{coin.balance}</td>
            <td>${coin.price.toLocaleString()}</td>
            <td>${(coin.balance * coin.price).toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default PortfolioTable;
