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


  useEffect(() => {
    axios.get('/api/', { withCredentials: true }).then((responce) => {
      setCards(responce.data)
    })
  }, [])

  return (
    <div className={classes.content_container}>
      <header className={classes.content_header}>
        <span className={classes.content_header_text}>
          Наши товары
        </span>
      </header >
      <div className={classes.content_catalog}>
        {test_data_chapters.map((chapter, index) => 
          <Chapter products={cards} name={chapter.name} addProduct={props.addProduct} key={index} windowWidth={props.windowWidth}/>
        )}
      </div>
    </div>
  );
}

export default Content;
