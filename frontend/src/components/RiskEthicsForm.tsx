import React, { useState } from "react";

const questions = {
  risk: [
    "I prefer stable, long-term cryptocurrency investments rather than frequently trading to maximize short-term gains.",
    "I am uncomfortable holding cryptocurrencies that can lose 50% of their value in a short period.",
    "I avoid investing in lesser-known cryptocurrencies with high potential but uncertain futures.",
    "If the market crashes and my portfolio loses 30% in a week, I would try and get out of my holdings.",
  ],
  ethical: [
    "I prefer blockchains that offset their carbon footprint through renewable energy projects even if they yield lower profits.",
    "Governments should regulate cryptocurrency projects to ensure they meet ethical and environmental standards.",
    "I prefer investing in cryptocurrencies that support social causes or fair distribution of wealth even if they yield lower profits.",
    "In regions with energy shortages, cryptocurrency mining should be limited.",
  ],
};

const RiskEthicsForm: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const [responses, setResponses] = useState<{ [key: string]: number }>({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  const allQuestions = [...questions.risk, ...questions.ethical];

  const handleResponse = (value: number) => {
    const updatedResponses = { ...responses, [allQuestions[currentQuestionIndex]]: value };
    setResponses(updatedResponses);

    if (currentQuestionIndex < allQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      // All questions answered, show final button
      setCurrentQuestionIndex(allQuestions.length);
    }
  };

  const handleSubmit = () => {
    const riskScores = questions.risk.map((q) => responses[q] || 1);
    const ethicalScores = questions.ethical.map((q) => responses[q] || 1);

    const riskAvg =
      (riskScores.reduce((a, b) => a + b, 0) - riskScores.length) /
      (4 * riskScores.length);
    const ethicalAvg =
      (ethicalScores.reduce((a, b) => a + b, 0) - ethicalScores.length) /
      (4 * ethicalScores.length);

    alert(`Risk Score: ${riskAvg.toFixed(2)}, Ethical Score: ${ethicalAvg.toFixed(2)}`);
    onClose();
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-white p-6">
      <div className="max-w-lg w-full bg-white shadow-md rounded-lg p-6 relative risk-ethics-popup">
        {currentQuestionIndex < allQuestions.length ? (
          <>
            <h2 className="text-xl font-bold mb-6 text-black text-center">
              Investment Risk & Ethics Questionnaire
            </h2>
            <p className="font-medium mb-10 text-black text-lg text-center">
              {allQuestions[currentQuestionIndex]}
            </p>
            <div className="button-group">
              {[
                { value: 1, label: "Strongly Disagree" },
                { value: 2, label: "Disagree" },
                { value: 3, label: "Neutral" },
                { value: 4, label: "Agree" },
                { value: 5, label: "Strongly Agree" },
              ].map(({ value, label }) => (
                <button
                  key={value}
                  onClick={() => handleResponse(value)}
                  className="response-button"
                >
                  {label}
                </button>
              ))}
            </div>
          </>
        ) : (
          <div className="text-center">
            <button onClick={handleSubmit} className="build-portfolio-button">
              Build My Portfolio!
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default RiskEthicsForm;
