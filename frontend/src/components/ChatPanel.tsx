import React, { useState } from 'react';

const ChatPanel: React.FC = () => {
  const [command, setCommand] = useState('');
  const [chatLog, setChatLog] = useState<string[]>([]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCommand(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Append the command to the chat log
    setChatLog([...chatLog, command]);
    setCommand('');
  };

  return (
    <div className="chat-panel">
      <h2>Ask About Your Portfolio</h2>
      <div className="chat-container">
        <div className="chat-log">
          {chatLog.map((msg, index) => (
            <div key={index} className="chat-message">
              {msg}
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="chat-input">
          <input
            type="text"
            placeholder="Type a command..."
            value={command}
            onChange={handleInputChange}
          />
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
};

export default ChatPanel;
