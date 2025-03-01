import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Form.css";

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

const RiskEthicsForm: React.FC = () => {
  const navigate = useNavigate();
  const [responses, setResponses] = useState<{ [key: string]: number }>({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [error, setError] = useState<string>("");
  const allQuestions = [...questions.risk, ...questions.ethical];

  const handleResponse = (value: number) => {
    const updatedResponses = { ...responses, [allQuestions[currentQuestionIndex]]: value };
    setResponses(updatedResponses);

    if (currentQuestionIndex < allQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      setCurrentQuestionIndex(allQuestions.length);
    }
  };

  const handleSubmit = async () => {
    const riskScores = questions.risk.map((q) => responses[q] || 1);
    const ethicalScores = questions.ethical.map((q) => responses[q] || 1);

    const riskAvg =
      (riskScores.reduce((a, b) => a + b, 0) - riskScores.length) /
      (4 * riskScores.length);
    const ethicalAvg =
      (ethicalScores.reduce((a, b) => a + b, 0) - ethicalScores.length) /
      (4 * ethicalScores.length);

    // alert(`Risk Score: ${riskAvg.toFixed(2)}, Ethical Score: ${ethicalAvg.toFixed(2)}`);
    try {
      // todo might need to change this endpoint
      const response = await fetch("/api/submit_user_scores", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ risk_score: riskAvg, ethics_score: ethicalAvg }),
      });

      if (!response.ok) {
        throw new Error("Failed to submit scores");
      }

      const data = await response.json();
      console.log("Submission successful:", data);
      alert("Scores submitted successfully!");
    } catch (err: any) {
      console.error(err);
      setError("Error submitting your scores. Please try again.");
    }
    navigate("/portfolio");
  };

  return (
    <div className="form-page">
      <div className="form-container">
        {currentQuestionIndex < allQuestions.length ? (
          <>
            <h2>Investment Risk & Ethics Questionnaire</h2>
            <p>{allQuestions[currentQuestionIndex]}</p>
            <div className="button-group">
              {[
                { value: 1, label: "Strongly Disagree" },
                { value: 2, label: "Disagree" },
                { value: 3, label: "Neutral" },
                { value: 4, label: "Agree" },
                { value: 5, label: "Strongly Agree" },
              ].map(({ value, label }) => (
                <button key={value} onClick={() => handleResponse(value)} className="response-button">
                  {label}
                </button>
              ))}
            </div>
          </>
        ) : (
          <div className="submit-container">
            <button onClick={handleSubmit} className="submit-button">
              Build My Portfolio!
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default RiskEthicsForm;
