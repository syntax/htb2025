import React, { useState, useEffect } from 'react';
import PortfolioSummary from './PortfolioSummary';
import PortfolioTable from './PortfolioTable';
import PhoneInfo from './PhoneInfo';
import ChatPanel from './ChatPanel';
import PieChartComponent from './Chart';
import ChartSelector from './ChartSelector';
import '../App.css';

const Portfolio: React.FC = () => {
  // State for each fetched data set.
  const [data, setData] = useState<any>(null);
  const [data2, setData2] = useState<any>(null);
  const [knnGraph, setKnnGraph] = useState<any>([]);
  // Initialize pred with empty objects for each prediction timeframe.
  const [pred, setPred] = useState<any>({
    pred_eod: {},
    pred_eow: {},
    pred_eom: {}
  });
  
  useEffect(() => {
    fetch("http://127.0.0.1:3332/portfolio/123")
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch(err => console.error("Error fetching portfolio data:", err));
  }, []);
  
  useEffect(() => {
    fetch("http://127.0.0.1:3332/get_portfolio_value_by_coin/123")
      .then((res) => res.json())
      .then((data2) => setData2(data2))
      .catch(err => console.error("Error fetching portfolio value:", err));
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:3332/api/get_knn_coords/123")
      .then((res) => res.json())
      .then((knnGraph) => setKnnGraph(knnGraph))
      .catch(err => console.error("Error fetching knn coords:", err));
  }, []);

  useEffect(() => {
    fetch("http://localhost:3332/api/generate_portfolio/123")
      .then((res) => res.json())
      .then((data) => setPred(data))
      .catch(err => console.error("Error fetching predictions:", err));
  }, []);

  return (
    <div className="page-container">
      <div className="app-container">
        <div className="content-wrapper">
          <div className="left-panel">
            {/* Check that data has loaded before rendering components */}
            {data && data2 ? (
              <>
                <PortfolioSummary data={data} data2={data2} />
                <PortfolioTable 
                  data={data} 
                  data2={data2} 
                  pred_eod={pred.pred_eod} 
                  pred_eow={pred.pred_eow} 
                  pred_eom={pred.pred_eom}
                />
                <ChartSelector 
                  holdings={data.holdings} 
                  holdings2={data2} 
                  knndata={knnGraph} 
                />
              </>
            ) : (
              <div>Loading portfolio...</div>
            )}
          </div>
          <div className="right-panel">
            <PhoneInfo />
            <ChatPanel data={data} data2={data2} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Portfolio;
