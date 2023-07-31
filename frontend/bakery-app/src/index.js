import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import axios from 'axios';
import { CookiesProvider } from 'react-cookie';

<<<<<<< HEAD

=======
>>>>>>> ef7aa5c71cb8d4c2e789057d72865ca2e8edc472
axios.defaults.withCredentials = true


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
        <CookiesProvider>
                <App />
        </CookiesProvider>
);
