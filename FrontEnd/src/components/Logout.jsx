// Logout.jsx
import React, { useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { logoutUser } from '../services/api'; 

const Logout = () => {
  const handleLogout = async () => {
    try {
      await logoutUser(); 
      window.location.href = '/login';e
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Logout;