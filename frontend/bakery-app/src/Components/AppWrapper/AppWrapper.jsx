import CaruselBox from '../CaruselBox/CaruselBox';
import Content from '../Content/Content';
import ModalBasket from '../ModalBasket/ModalBasket';
import Footer from '../Footer/Footer';
import Header from '../Header/Header';
import Navbar from '../Navbar/Navbar';
import classes from './AppWrapper.module.css';
import React, { useEffect, useState } from 'react';
import { Route, Routes, useParams } from 'react-router-dom';
import ModalWindow from '../ModalWindow/ModalWindow';
import axios from 'axios';

import { useNavigate } from "react-router-dom";
import Profile from '../Profile/Profile';


function AppWrapper(props) {




  //Запрос, на то, зарегался ли человек

  const { token } = useParams();


  console.log(token);

  // const requestForSuccessfulRegistaration = () => {
  //   if (token) {
  //     axios.post(`/register/${token}`, { token: token }).then((responce) => {
  //       props.authorization.authorize(responce.data.data)
  //     })
  //   if (!props.authorization.isAuthorizated) {
  //     if (token) {
  //       console.log('Отправка данных на сервер')
  //       axios.post(`/auth/token_register`, { token: token }).then((responce) => {
  //         console.log('Обработка данных с сервера')
  //         props.authorization.authorize(responce.data.data)

  //         navigate("/");

  //         console.log('Текущие куки:');
  //         console.log();
  //       })
  //     // } else if (cookies.token) {
  //     //   console.log('Отправка данных на сервер, если есть куки')
  //     //   axios.get(`/auth/token`, { token: cookies.token }).then((responce) => {
  //     //     console.log('Обработка данных с сервера')
  //     //     props.authorization.authorize(responce.data.data)

  //     //     console.log('Текущие куки:');
  //     //     console.log(cookies);
  //     //   })
  //       }
  //     }
  //   }
  // }

  // requestForSuccessfulRegistaration()
  

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




  //Отвечает за октрытие/закрытие модлаьного окна корзины, меняя правый паддинг и скрывая содержимое за экраном
  const [style, setStyle] = useState({ overflowY: 'scroll' })
  const [isModalBasketOpen, setModalBasketOpen] = useState(false)

  const changeModalWindow = () => {
    setModalBasketOpen((isModalBasketOpen) => !isModalBasketOpen);

    if (!isModalBasketOpen) {
      setStyle({ overflowY: 'hidden', paddingRight: 17 })
    } else {
      setStyle({ overflowY: 'scroll', paddingRight: 0 })
    }
  }
  //Корзина и продукты в ней
  const [basketProducts, setBasketProducts] = useState([])
  useEffect(() => {
    /*axios.get('/basket/products').then((responce) => {
      setBasketProducts(responce.data)
    })*/
  })




  //Другие модальные окна
  const [typeModalWindow, setTypeModalWindow] = useState('')
  const MODAL_AUTHORIZATION = 'MODAL_AUTHORIZATION'
  const MODAL_REGISTRATION = 'MODAL_REGISTRATION'

  const changeTypeModalWindow = (type) => {
    setTypeModalWindow(type)
  }

  const closeModalWindow = () => {
    setTypeModalWindow('');
  }

  const mainPage = (
    <React.Fragment>
      <ModalBasket
        basketProducts={/*basketProducts*/test_data}
        changeModalWindow={changeModalWindow}
        isModalBasketOpen={isModalBasketOpen} />

      {typeModalWindow && <ModalWindow
        type={typeModalWindow}
        types={{ MODAL_AUTHORIZATION: MODAL_AUTHORIZATION, MODAL_REGISTRATION: MODAL_REGISTRATION }}
        closeModalWindow={closeModalWindow}
        functions={{ requestForSuccessfulRegistaration: ''/*requestForSuccessfulRegistaration*/ }}
        changeTypeModalWindow={changeTypeModalWindow}
        authorization={props.authorization} />}
      <Header
        types={{ MODAL_AUTHORIZATION: MODAL_AUTHORIZATION }}
        changeTypeModalWindow={changeTypeModalWindow}
        isAuthorizated={props.authorization.isAuthorizated} />
      <Navbar changeModalWindow={changeModalWindow} />
      {true ? <Profile/> :
      <React.Fragment>
      <CaruselBox />
      <Content products={test_data} />
      </React.Fragment>
      }
      <Footer />
    </React.Fragment>
  )

  const profilePage = (
    <React.Fragment>
      <Header
        types={{ MODAL_AUTHORIZATION: MODAL_AUTHORIZATION }}
        changeTypeModalWindow={changeTypeModalWindow}
        isAuthorizated={props.authorization.isAuthorizated} />
      <div>

      </div>
      <Footer />
    </React.Fragment>
  )


  return (
    <div className={classes.wrapper} style={style}>
      <Routes>
        <Route path='/*' element={mainPage} />
        <Route path='/profile' element={''} />
      </Routes>
    </div>
  );
}

export default AppWrapper;
