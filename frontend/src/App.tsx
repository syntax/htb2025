import React from 'react';
import PortfolioSummary from './components/PortfolioSummary';
import PortfolioTable from './components/PortfolioTable';
import PhoneInfo from './components/PhoneInfo';
import ChatPanel from './components/ChatPanel';
import './App.css';

export interface CryptoCoin {
  id: number;
  name: string;
  symbol: string;
  balance: number;
  price: number;
}

const portfolioData: CryptoCoin[] = [
  { id: 1, name: 'Bitcoin', symbol: 'BTC', balance: 1.234, price: 30000 },
  { id: 2, name: 'Ethereum', symbol: 'ETH', balance: 10, price: 2000 },
  { id: 3, name: 'Cardano', symbol: 'ADA', balance: 5000, price: 1.2 },
];

interface SummaryStats {
  totalValue: number;
  riskLevel: string;
  bestPerformer: string;
  worstPerformer: string;
}

const calculateSummaryStats = (portfolio: CryptoCoin[]): SummaryStats => {
  const totalValue = portfolio.reduce(
    (acc, coin) => acc + coin.balance * coin.price,
    0
  );
  return {
    totalValue,
    riskLevel: 'Medium', // Placeholder
    bestPerformer: portfolio[0].name, // Placeholder
    worstPerformer: portfolio[portfolio.length - 1].name, // Placeholder
  };
};

const App: React.FC = () => {
  const stats = calculateSummaryStats(portfolioData);

  return (
    <div className="page-container">
      <div className="app-container">
        <h3>At a glance...</h3>
        <div className="content-wrapper">
          <div className="left-panel">
            <PortfolioSummary stats={stats} />
            <PortfolioTable portfolio={portfolioData} />
          </div>
          <div className="right-panel">
            <PhoneInfo />
            <ChatPanel />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
