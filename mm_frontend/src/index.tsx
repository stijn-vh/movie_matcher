import React, { useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { Main } from './screens/main/main';
import { firebaseConfig } from './utils/firebase';
import { getAuth } from "firebase/auth";

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app)


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