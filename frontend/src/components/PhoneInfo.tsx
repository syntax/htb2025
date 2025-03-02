import React, { useState, useEffect } from 'react';

const PhoneInfo: React.FC = () => {
  const [phone, setPhone] = useState('+44');
  const [submittedPhone, setSubmittedPhone] = useState('');

  useEffect(() => {
    const fetchPhoneNumber = async () => {
      try {
        const response = await fetch(`http://localhost:3332/api/get_user_phone_number/123`);
        if (!response.ok) throw new Error('Failed to fetch');
        
        const data = await response.json();
        if (data.phone_number) {
          setSubmittedPhone(data.phone_number);
          setPhone(data.phone_number);
        }
      } catch (error) {
        console.error('Error fetching phone number:', error);
      }
    };
    fetchPhoneNumber();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let value = e.target.value;
    value = value.replace(/[^+\d]/g, '');
    if (!value.startsWith('+44')) {
      value = '+44' + value.replace(/^\+*/, '');
    }
    if (value.length > 13) {
      value = value.slice(0, 13);
    }
    setPhone(value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    fetch('http://127.0.0.1:3332/api/submit_user_phone_number', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: '123', phone_number: phone })
    })
    setSubmittedPhone(phone);
    setPhone('+44');
  };

  const handleRemove = async () => {
    try {
      const response = await fetch('http://localhost:3332/api/submit_user_phone_number', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: '123', phone_number: '' })
      });

      if (!response.ok) throw new Error('Removal failed');
      
      setSubmittedPhone('');
      setPhone('+44');
    } catch (error) {
      console.error('Error removing phone number:', error);
      alert('Failed to remove phone number. Please try again.');
    }
  };

  return (
    <div className="phone-info-panel">
      <h2>Rug Pull / AtypicalVol SMS Alerts</h2>
      {!submittedPhone ? (
        <form onSubmit={handleSubmit}>
          <div className="phone-input-container">
            <input
              type="tel"
              placeholder="Enter your phone number"
              value={phone}
              onChange={handleInputChange}
              className="phone-input"
            />
            <button type="submit" className="phone-button">
              Submit
            </button>
          </div>
        </form>
      ) : (
        <div className="phone-input-container">
          <div className="phone-status-group">
            <p className="phone-display">Phone number: {submittedPhone}</p>
            <div className="active-status">
              <span className="checkmark">✓</span>
              <span className="active-text">Active</span>
            </div>
          </div>
          <button type="button" onClick={handleRemove} className="phone-button">
            Remove
          </button>
        </div>
      )}
    </div>
  );
};

export default PhoneInfo;
