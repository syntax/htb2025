import React from 'react';
import { Link } from 'react-router-dom';
import './Welcome.css';

const Welcome: React.FC = () => {
  return (
    <div className="welcome-page">
      <h1>Welcome to Our Site!</h1>
      <p>
        This is a short introduction to our platform. Get ready to explore your investment risk and ethics.
      </p>
      <div className="welcome-buttons">
        <Link to="/form">
          <button className="welcome-button">
            Take Risk & Ethics Questionnaire
          </button>
        </Link>
      </div>
    </div>
  );
};

export default Welcome;
