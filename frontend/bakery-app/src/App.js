import { useEffect, useRef, useState } from 'react';
import './App.css';
import AppWrapper from './Components/AppWrapper/AppWrapper';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

function App() {

  //Routing
  const router = createBrowserRouter([
    {
      path: '/',
      element: <AppWrapper/>
    }
  ])



  return (
    <div className="App">
      <RouterProvider router={router}/>
    </div>
  );
}

export default App;
