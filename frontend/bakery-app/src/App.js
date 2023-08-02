import { useEffect, useState } from 'react';
import './App.css';
import AppWrapper from './Components/AppWrapper/AppWrapper';
import { RouterProvider, createBrowserRouter} from 'react-router-dom';
import Cookies from 'js-cookie'
import axios from 'axios';

 
let login;

function App() {

  const [userType, setUserType] = useState('')
  
  useEffect(() => {
      if (Cookies.get('remember_token2') === undefined) {
        setUserType('');
        setIsAuthorizated(false)
      } else if (Cookies.get('remember_token2') === 'user') {
        setUserType('user');
        setIsAuthorizated(true);
      } else if (Cookies.get('remember_token2') === 'restaurant') {
        setUserType('restaurant')
        setIsAuthorizated(true);
      } else if (Cookies.get('remember_token2') === 'main_admin') {
        setUserType('main_admin')
        setIsAuthorizated(true);
      } else {
        alert('Неизвестный пользователь')
      }
  })
  
  
  const [isAuthorizated, setIsAuthorizated] = useState(false)
  
  const authorize = (loginText) => {
    if (loginText === 'user@mail.ru') {
      setUserType('user')
    } else if (loginText === 'restaurant@mail.ru') {
      setUserType('restaurant') 
    } else if (loginText === 'adcde@mail.ru') {
      setUserType('main_admin') 
    }
    setIsAuthorizated(true)
    login = loginText;
  }

  const unAuthorize = () => {
    axios.get('auth/logout').then(() => {      
      setIsAuthorizated(false)
      login = null;
    }) 
  }




  //Routing
  const router = createBrowserRouter([
    {
      path: '*',
      element: <AppWrapper authorization={{isAuthorizated: isAuthorizated, authorize:authorize, userType: userType, setUserType: setUserType, unAuthorize: unAuthorize}} />
    }
  ])


  return (
    <div className="App">
      <RouterProvider router={router}/>
    </div>
  );
}

export default App;
