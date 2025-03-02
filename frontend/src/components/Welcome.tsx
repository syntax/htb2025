import React from 'react';
import { Link } from 'react-router-dom';
import './Welcome.css';
import quintinGif from './quintin.gif';

const Welcome: React.FC = () => {
  return (
    <div className="welcome-container">
      {/* Left Text Section */}
      <div className="welcome-left">
        <h1 className="welcome-title">Hi, I am Quintin</h1>
        <p className="welcome-subtitle">
         I'm an AI-powered cryptocurrency portfolio manager that tailors your investments based on your risk tolerance and ethical values. Through building a portfolio that reflects what matters most to you, you can confidently buy, sell, and track your assets over time. With future price predictions and personalized SMS and phone call updates, I'll help you to stay informed every step of the way!
        </p>
        <div className="welcome-buttons">
          <Link to="/form">
            <button>Take Risk &amp; Ethics Questionnaire</button>
          </Link>
        </div>
      </div>

      {/* Right Image Section */}
      <div className="welcome-right">
        <img
          src={quintinGif}
          alt="App Preview"
          className="welcome-image"
        />
      </div>
    </div>
  );
};

export default Welcome;
