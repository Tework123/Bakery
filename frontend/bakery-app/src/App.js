import { useEffect, useRef, useState } from 'react';
import './App.css';
import AppWrapper from './Components/AppWrapper/AppWrapper';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

let login;

function App() {


  const [isAuthorizated, setIsAuthorizated] = useState(false)
  
  const authorize = (loginText) => {
    setIsAuthorizated(true)
    login = loginText;
  }

  const unAuthorize = () => {
    setIsAuthorizated(false)
    login = null;
  }

  //Routing
  const router = createBrowserRouter([
    {
      path: '/:token',
      element: <AppWrapper authorization={{isAuthorizated: isAuthorizated, authorize:authorize}} />
    },
    {
      path: '/',
      element: <AppWrapper authorization={{isAuthorizated: isAuthorizated, authorize:authorize}} />
    }
  ])

//  useEffect(() => {
//    axios.get("/main/").then((response) => {
//      setCurrentTime(response.data.data);
//    });
//  }, []);
//
//  useEffect(() => {
//    axios.get("/admin/").then((response) => {
//      setCurrentTime3(response.data.data);
//    });
//  }, []);
//
//
//
//
//
//  const changeLogin = (e) => {
//    console.log(e.target.value);
//    setLogin(e.target.value)
//  }
//
//  const changeRegister = (e) => {
//    console.log(e.target.value);
//    setRegister(e.target.value)
//  }
//
//  function sendLogin() {
//    axios.post('/auth/login', {login: login}).then((response) => {console.log(response.data.data)})
//
//  }
//
//    function sendRegister() {
//    axios.post('/auth/register', {register: register}).then((response) => {console.log(response.data.data)})
//
//  }




  return (
    <div className="App">
      <RouterProvider router={router}/>
    </div>
  );
}

export default App;
