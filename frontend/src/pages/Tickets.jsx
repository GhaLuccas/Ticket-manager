// Tickets.jsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Tickets = () => {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const response = await axios.get('http://localhost:8000/tickets/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        setTickets(response.data.ticket_list);
      } catch (error) {
        console.error('Failed to fetch tickets:', error);
      }
    };
    fetchTickets();
  }, []);

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">Tickets</h1>
      <ul className="list-group">
        {tickets.map((ticket) => (
          <li key={ticket.id} className="list-group-item">
            <h2>{ticket.problem}</h2>
            <p>{ticket.solution || 'No solution yet'}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Tickets;