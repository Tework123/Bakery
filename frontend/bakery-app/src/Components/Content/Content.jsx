import { useEffect, useState } from 'react';
import Chapter from './Chapter/Chapter';
import classes from './Content.module.css';
import axios from 'axios';

function Content(props) {


  const [cards, setCards] = useState([])
  const test_data_chapters = [
    {
      name: 'Выпечка'
    },
    {
      name: 'Хлебушек'
    },
    {
      name: 'Пироги'
    },
    {
      name: 'Десерты'
    }
  ]

 


  const [login, setlogin] = useState('')
  function sendEmailRegistr() {
    axios.post('/auth/login_code', { code: login }).then((response) => {

      console.log(response.data.data)
      props.requestForSuccessfulRegistaration()
    })
  } 

  const onClickRegistr = () => {
    sendEmailRegistr()
  }
  const onChangeLogin = (e) => {
    setlogin(e.target.value)
  } 


  useEffect(() => {
    axios.get('/main').then((responce) => {
      setCards(responce.data)
    })
  }, [])

  return (
    <div className={classes.content_container}>
            <input className={classes.authoriaion_input_item} placeholder='Код' onChange={(e) => onChangeLogin(e)}></input>
            <div className={classes.authoriaion_enter} onClick={onClickRegistr}>Отправить код</div>
      <header className={classes.content_header}>
        <span className={classes.content_header_text}>
          Наши товары
        </span>
      </header >
      <div className={classes.content_catalog}>
        {test_data_chapters.map((chapter, index) => 
          <Chapter products={cards} name={chapter.name} addProduct={props.addProduct} key={index}/>
        )}
      </div>
    </div>
  );
}

export default Content;
