import React, { useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { Main } from './screens/main/main';

const App = () => {
  return (
    <React.StrictMode>
      <Main />
    </React.StrictMode>
  );
};

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(<App />);