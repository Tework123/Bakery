import CaruselBox from '../CaruselBox/CaruselBox';
import Content from '../Content/Content';
import ModalBasket from '../ModalBasket/ModalBasket';
import Footer from '../Footer/Footer';
import Header from '../Header/Header';
import Navbar from '../Navbar/Navbar';
import classes from './AppWrapper.module.css';
import { useState } from 'react';
import { Route, createBrowserRouter, createRoutesFromElements } from 'react-router-dom';
import ModalWindow from '../ModalWindow/ModalWindow';

function AppWrapper(props) {





  const test_data = [
    {
      name: 'Булочка с корицей',
      price: 100,
      description: 'Очень вкусная булочка, всем советую',
      id: 0,
      imageURL: '',
      quantity: 1,
    },
    {
      name: 'Булочка с вишней',
      price: 10,
      description: 'Не очень вкусная булочка, всем советую',
      id: 1,
      imageURL: '',
      quantity: 2,
    },
    {
      name: 'Булочка с ягодами',
      price: 1000,
      description: 'Очень вкусная булочка, всем не советую',
      id: 2,
      imageURL: '',
      quantity: 3,
    },
    {
      name: 'Пирог',
      price: 50,
      description: 'Кайф',
      id: 3,
      imageURL: '',
      quantity: 0,
    },
    {
      name: 'Булочка с корицей',
      price: 100,
      description: 'Очень вкусная булочка, всем советую',
      id: 4,
      imageURL: '',
      quantity: 0
    },
    {
      name: 'Булочка с корицей',
      price: 100,
      description: 'Очень вкусная булочка, всем советую',
      id: 5,
      imageURL: '',
      quantity: 0
    },
    {
      name: 'Булочка с корицей',
      price: 100,
      description: 'Очень вкусная булочка, всем советую',
      id: 5,
      imageURL: '',
      quantity: 0
    },
  ]





  createBrowserRouter(
    createRoutesFromElements(
      <Route

       
      />
    )
  )







  //Отвечает за октрытие/закрытие модлаьного окна корзины, меняя правый паддинг и скрывая содержимое за экраном
  const [style, setStyle] = useState({ overflowY: 'scroll' })
  const [isModalBasketOpen, setModalBasketOpen] = useState(false)

  const changeModalWindow = () => {
    console.log(isModalBasketOpen);
    setModalBasketOpen((isModalBasketOpen) => !isModalBasketOpen);

    if (!isModalBasketOpen) {
      setStyle({ overflowY: 'hidden', paddingRight: 17 })
    } else {
      setStyle({ overflowY: 'scroll', paddingRight: 0 })
    }
    console.log(isModalBasketOpen);
  }




  //Другие модальные окна
  const [isModalWindowOpen, setModalWindowOpen] = useState(false)
  const MODAL_AUTHORIZATION = 'MODAL_AUTHORIZATION'
  const MODAL_REGISTRATION = 'MODAL_REGISTRATION'
  let typeModalWindowOpen;

  const openModalWindow = (type) => {
    setModalWindowOpen(true)
    typeModalWindowOpen = type;
  }

  const closeModalWindow = () => {
    setModalWindowOpen(false);
    typeModalWindowOpen = null;
  }



  return (
    <div className={classes.wrapper} style={style}>
      <ModalBasket
        basketProducts={test_data}
        changeModalWindow={changeModalWindow}
        isModalBasketOpen={isModalBasketOpen}/>

      {isModalWindowOpen && <ModalWindow
                              type={typeModalWindowOpen}
                              types={{MODAL_AUTHORIZATION: MODAL_AUTHORIZATION, MODAL_REGISTRATION: MODAL_REGISTRATION}}
                              closeModalWindow={closeModalWindow}
                              authorization={props.authorization}/>}

      <Header
        types={{MODAL_AUTHORIZATION: MODAL_AUTHORIZATION}}
        openModalWindow={openModalWindow}
        isAuthorizated={props.authorization.isAuthorizated}/>
      <Navbar changeModalWindow={changeModalWindow}/>
      <CaruselBox />
      <Content products={test_data} />
      <Footer />
    </div>
  );
}

export default AppWrapper;
