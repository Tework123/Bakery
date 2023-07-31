import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import axios from 'axios';
import { CookiesProvider } from 'react-cookie';


axios.defaults.withCredentials = true


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
        <CookiesProvider>
                <App />
        </CookiesProvider>
);
