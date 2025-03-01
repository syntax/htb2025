// src/components/Welcome.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import './Welcome.css'; // Optional: create a separate CSS file for welcome styles

const Welcome: React.FC = () => {
  return (
    <div className="welcome-page">
      <h1>Welcome to Our Site!</h1>
      <p>
        This is a short introduction to our platform. Get ready to find out more about your investment risk and ethics.
      </p>
      <Link to="/riskethicquiz">
        <button className="welcome-button">
          Take Risk & Ethics Questionnaire
        </button>
      </Link>
    </div>
  );
};

export default Welcome;
