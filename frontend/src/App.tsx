import { React, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Welcome from './components/Welcome';
import RiskEthicsForm from './components/Form';
import Portfolio from './components/Portfolio';

const App: React.FC = () => {

  useEffect(() => {
    // Using Fetch API to call the backend endpoint on initial load
    fetch('http://127.0.0.1:3332/store_crypto_data')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        console.log('Crypto data stored successfully:', data);
      })
      .catch((error) => {
        console.error('Error fetching crypto data:', error);
      });
  }, []);
  
  return (
    <Routes>
      <Route path="/" element={<Welcome />} />
      <Route path="/form" element={<RiskEthicsForm />} />
      <Route path="/portfolio" element={<Portfolio />} />
    </Routes>
  );
};

export default App;
