import CaruselBox from '../CaruselBox/CaruselBox';
import Content from '../Content/Content';
import ModalBasket from '../ModalBasket/ModalBasket';
import Footer from '../Footer/Footer';
import Header from '../Header/Header';
import Navbar from '../Navbar/Navbar';
import classes from './AppWrapper.module.css';
import React, { useEffect, useState } from 'react';
import { Route, Routes} from 'react-router-dom';
import ModalWindow from '../ModalWindow/ModalWindow';
import Profile from '../Profile/Profile';
import axios from 'axios';
import { useResize } from '../../Hooks/useResize';

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


  const windowWidth = useResize();


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
    if (props.authorization.isAuthorizated) {
      axios.get('/basket').then((responce) => {
        setBasketProducts(responce.data)
      })
    }
  }, [])


  //функции отвечающие за добавление и удаление товаров корзины
  const changeBasket = ({ action, id }) => {

    axios.patch('/basket', {action:action, card_id: id}).then((responce) => {
      let newBasket = [...basketProducts];
      let changeIndex = null;
  
      basketProducts.forEach((element, index) => {
        if (element.card_id === id) {
          changeIndex = index;
        }
      });
      
      if (action === '+') {
        newBasket[changeIndex].amount++;
      } else if (action === '-') {
        if (newBasket[changeIndex].amount === 1) {
          newBasket.splice(changeIndex, 1);
        } else {
          newBasket[changeIndex].amount--;
        }
      }
      setBasketProducts(newBasket);
    })
    
  }

  const addProduct = (product) => {
    console.log(product);
    axios.patch('/basket', {action:'+', card_id: product.card_id}).then(() => {
    if (props.authorization.isAuthorizated) {
      let newBasket = [...basketProducts];
      let changeIndex = null;

      basketProducts.forEach((element, index) => {
        if (element.card_id === product.card_id) {
          changeIndex = index;
        }
      
      });

      if (changeIndex === null) {
        newBasket.push({...product, amount: 1});
      } else {
        newBasket[changeIndex].amount++;
      }
      setBasketProducts(newBasket)
    } else {
      alert('Нельзя пока не авторизован')
    }
  })
  }



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
        changeModalWindow={changeModalWindow}
        isModalBasketOpen={isModalBasketOpen}
        changeBasket={changeBasket} 
        basketProducts={basketProducts}
        isAuthorizated={props.authorization.isAuthorizated}/>
        

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
      <CaruselBox />
      <Content products={test_data} addProduct={addProduct} windowWidth={windowWidth}/>
      <Footer />
    </React.Fragment>
  )

  const profilePage = (
    <React.Fragment>
      <Header
        types={{ MODAL_AUTHORIZATION: MODAL_AUTHORIZATION }}
        changeTypeModalWindow={changeTypeModalWindow}
        isAuthorizated={props.authorization.isAuthorizated} />
      <Profile authorization={props.authorization}/>
      <Footer />
    </React.Fragment>
  )


  return (
    <div className={classes.wrapper} style={style}>
      <Routes>
        <Route path='/profile/*' element={profilePage} />
        <Route path='/*' element={mainPage} />        
      </Routes>
    </div>
  );
}

export default AppWrapper;
