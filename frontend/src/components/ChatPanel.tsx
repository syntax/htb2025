import React, { useState, useRef, useEffect } from 'react';

const ChatPanel: React.FC = ({data, data2}) => {
  const [command, setCommand] = useState('');
  const [chatLog, setChatLog] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const chatLogRef = useRef<HTMLDivElement>(null);
  const [typingIndicator, setTypingIndicator] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCommand(e.target.value);
  };
  
  


  useEffect(() => {
    if (loading) {
      let dots = '';
      const interval = setInterval(() => {
        dots = dots.length < 3 ? dots + '~' : '';
        setTypingIndicator(`Quentin is typing${dots}`);
      }, 500);
      return () => clearInterval(interval);
    } else {
      setTypingIndicator('');
    }
  }, [loading]);

  const fetchChatResponse = async (userCommand: string): Promise<string> => {
    const prompt = createCryptoAdvisorProfile(data, data2, userCommand);
    console.log(prompt);
    setLoading(true);
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
    try {
      const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          model: "gpt-4o-mini",
          messages: [{ role: "assistant", content: prompt }],
          temperature: 0.7,
        })
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      
      const data = await response.json();
      return data.choices[0].message.content;
    } catch (error) {
      console.error("Error fetching chat response:", error);
      return "Error: Unable to fetch response from OpenAI.";
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const userMessage = command;
    setChatLog(prev => [...prev, `User: ${userMessage}`]);
    setCommand('');

    const botResponse = await fetchChatResponse(userMessage);
    setChatLog(prev => [...prev, `Quentin: ${botResponse}`]);
  };

  useEffect(() => {
    if (chatLogRef.current) {
      chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
    }
  }, [chatLog, loading]);

  return (
    <div className="chat-panel">
      <h2>Ask About Your Portfolio</h2>
      <div className="chat-container">
        <div className="chat-log" ref={chatLogRef} style={{ maxHeight: '650px', overflowY: 'auto' }}>
          {chatLog.map((msg, index) => (
            <div key={index} className="chat-message">
              {msg}
            </div>
          ))}
          {loading && (
            <div className="loading-bar">
              <div className="typing-indicator">{typingIndicator}</div>
            </div>
          )}
        </div>
        <form onSubmit={handleSubmit} className="chat-input">
          <input
            type="text"
            placeholder="Type a command..."
            value={command}
            onChange={handleInputChange}
            disabled={loading}
          />
          <button type="submit" disabled={loading}>Send</button>
        </form>
      </div>

      <style>{`
        .loading-bar {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 30px;
          margin-top: 10px;
        }

        .typing-indicator {
          font-style: italic;
          font-weight: bold;
          animation: fadeInOut 1s infinite;
        }

        @keyframes fadeInOut {
          0% { opacity: 1; }
          50% { opacity: 0.5; }
          100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
};

interface UserData {
  holdings: { [key: string]: number };
  total_ethics: number;
  total_risk: number;
  user_id: number;
}

interface UpdatedHoldings {
  [key: string]: number;
}

const createCryptoAdvisorProfile = (
  data: UserData,
  data2: UpdatedHoldings,
  clientMessage: string
): string => {
  return `
YOUR NAME IS QUENTIN AND YOU ARE A PERSONAL CRYPTO PORTFOLIO MANAGER.
Your purpose is to give advice regarding potential investment opportunities 
with a focus on risk appetite, sustainability, and ethics, 
in accordance with your client's particular tastes. 

Many of your clients will be from groups less crypto-inclined, 
such as older persons.

In particular, your client in this case has the following tastes:

(Scores are given as a range 0-1)

Your client has a risk appetite of ${data.total_risk}, where 1 is very risk averse.
Your client has an ethical appetite of ${data.total_ethics}, where 1 means they care a lot 
about ethical considerations and sustainability.

The user's current portfolio includes:
Holdings: ${JSON.stringify(data.holdings, null, 2)}
Updated Holdings: ${JSON.stringify(data2, null, 2)}

Be sure to consider these user-specific details when giving advice.

Your client has sent you the following message, please respond to the best 
of your ability such that they receive an answer they want, 
whilst maintaining brevity:

${clientMessage}
  `;
};


export default ChatPanel;