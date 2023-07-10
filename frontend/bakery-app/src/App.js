import { useEffect, useRef, useState } from 'react';
import './App.css';
import AppWrapper from './Components/AppWrapper/AppWrapper';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

function App() {


  let size = 20;
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      if ()
      console.log("");
    }
  }



  const [scroll, setScroll] = useState(0);

  useEffect(() => {
    window.addEventListener("scroll", () => {
      setScroll(window.scroll)
      console.log(scroll);
    })
      
      return () => window.removeEventListener("scroll", () => {
        setScroll(window.scroll)
      })
    }, []);
  





  //Отвечает за октрытие/закрытие модлаьного окна корзины, меняя правый паддинг и скрывая содержимое за экраном
  const [style, setStyle] = useState({overflowY:'scroll'})
  const [isModalBasketOpen, setModalBasketOpen] = useState(false)

  const changeModalWindow = () => {
    
    debugger
    console.log("До " + isModalBasketOpen);
    setModalBasketOpen(!isModalBasketOpen);
    console.log("После " + isModalBasketOpen);
    debugger
    if (!isModalBasketOpen) {
      setStyle({overflowY:'hidden', paddingRight: 17})
    } else {
      setStyle({overflowY:'scroll', paddingRight: 0})
    }
    console.log(isModalBasketOpen);
    console.log(style);
  }



  //Routing
  const router = createBrowserRouter([
    {
      path: '/',
      element: <AppWrapper changeModalWindow={changeModalWindow} isModalBasketOpen={isModalBasketOpen}/>
    }
  ])



  return (
    <div className="App" style={style}>
      <RouterProvider router={router}/>
    </div>
  );
}

export default App;
