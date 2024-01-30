import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';


function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:5000/login_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        
        localStorage.setItem('access_token', data.access_token);
        navigate('/UserDashboard'); 
      } else {
        const data = await response.json();
        setError(data.message);
      }
    } catch (error) {
      setError('An error occurred. Please try again later.');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
  <div className="card" style={{ boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2)', borderRadius: '8px', padding: '20px', width: '60%', maxWidth: '400px' }}>
    <h1 style={{ textAlign: 'center', color:'magenta' }}>Login</h1>
    <form onSubmit={handleSubmit}>
      {error && <p className="error-message">{error}</p>}
      <div className="form-group">
        <input
          type="text"
          name="email"
          value={formData.email}
          placeholder="Email"
          onChange={handleChange}
          style={{ fontSize: '14px', color: 'magenta' }}
        />
      </div>
      <div className="form-group">
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          style={{ fontSize: '14px', color: 'magenta' }}
        />
      </div>
      <button type="submit" style={{ fontSize: '14px', color: 'magenta' }}>Login</button>
    </form>
  </div>
</div>

  );
}

export default Login;
