import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import PortfolioSummary from './components/PortfolioSummary';
import PortfolioTable from './components/PortfolioTable';
import PhoneInfo from './components/PhoneInfo';
import ChatPanel from './components/ChatPanel';
import RiskEthicsForm from './components/RiskEthicsForm';
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
  const [isFormOpen, setIsFormOpen] = useState(false);

  return (
    <Router>
      <div className={`page-container ${isFormOpen ? 'blurred' : ''}`}>
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
          <div className="mt-4 text-center">
            <button
              onClick={() => setIsFormOpen(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Take Risk & Ethics Questionnaire
            </button>
          </div>
        </div>
      </div>
      
      {isFormOpen && (
        <div className="popup-overlay" onClick={() => setIsFormOpen(false)}>
          <div className="popup-container" onClick={(e) => e.stopPropagation()}>
            <RiskEthicsForm onClose={() => setIsFormOpen(false)} />
          </div>
        </div>
      )}
    </Router>
  );
};

export default App;
