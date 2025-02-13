// App.jsx

import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Tickets from './pages/Tickets';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/tickets" element={<Tickets />} />
    </Routes>
  );
};

export default App;