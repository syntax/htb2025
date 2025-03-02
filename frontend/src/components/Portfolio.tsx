import React, { use } from 'react';
import { useState, useEffect } from 'react';
import PortfolioSummary from './PortfolioSummary';
import PortfolioTable from './PortfolioTable';
import PhoneInfo from './PhoneInfo';
import ChatPanel from './ChatPanel';
import PieChartComponent from './Chart';
import ChartSelector from './ChartSelector';
import '../App.css';


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

const Portfolio: React.FC = () => {
  const stats = calculateSummaryStats(portfolioData);

  const [data, setData] = useState([]);
  const [data2 , setData2] = useState([]);
  const [knnGraph, setKnnGraph] = useState([]);
  const [pred, setPred] = useState([]);
  
  useEffect(() => {
    fetch("http://127.0.0.1:3332/portfolio/123")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);
  

  useEffect(() => {
    fetch("http://127.0.0.1:3332/get_portfolio_value_by_coin/123")
      .then((res) => res.json())
      .then((data2) => setData2(data2));
  }, []);

  useEffect(() => {
    fetch("http:///127.0.0.1:3332/api/get_knn_coords/123")
      .then((res) => res.json())
      .then((knnGraph) => setKnnGraph(knnGraph));
  }, );

  useEffect(() => {
    fetch("http://localhost:3332/api/generate_portfolio/123")
    .then((res) => res.json())
    .then((data) => setPred(data));
  }, []);

  return (
    <div className="page-container">
      <div className="app-container">
        <div className="content-wrapper">
          <div className="left-panel">
            <PortfolioSummary data={data} data2={data2} />
            <PortfolioTable data = {data} data2 = {data2} pred = {pred}/>
            <ChartSelector holdings = {data.holdings} holdings2 = {data2} knndata = {knnGraph} />
          </div>
          <div className="right-panel">
            <PhoneInfo />
            <ChatPanel data = {data} data2 = {data2}/>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Portfolio;
