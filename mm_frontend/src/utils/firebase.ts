export const firebaseConfig = {
  apiKey: "AIzaSyCV0ZPfn70WefU9IizwJ1_60fGxCNS6Krw",
  authDomain: "moviematcher-51a2a.firebaseapp.com",
  projectId: "moviematcher-51a2a",
  storageBucket: "moviematcher-51a2a.firebasestorage.app",
  messagingSenderId: "737120185483",
  appId: "1:737120185483:web:1002490c14c1f78624788e",
  measurementId: "G-3ZNKE988Q2"
};

import { getAuth } from "firebase/auth";

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
import { getMessaging } from "firebase/messaging";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional


// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const analytics = getAnalytics(app);
export const auth = getAuth(app)
export const db = getFirestore(app)
export const messaging = getMessaging(app)
