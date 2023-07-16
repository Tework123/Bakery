import { useEffect, useState } from 'react';
import Chapter from './Chapter/Chapter';
import classes from './Content.module.css';
import axios from 'axios';

function Content(props) {

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

  const [cards, setCards] = useState([])
  const [selectedImage, setSelectedImage] = useState(null);


  const chooseFileImage = (e) => {
    setSelectedImage(e.target.files[0])
    console.log(e.target.files[0]);

  }

  const submitImage = () => {
    const formData = new FormData();
    console.log(selectedImage);
    formData.append('card_image', selectedImage);
    axios.post('/admin/cards', formData).then((response) => {
      console.log(response)
  
      })
  }



  useEffect(() => {
    // axios.get('/admin/cards').then((response) => {
    //   setCards(response.data)
    // })
  }, [])

  return (
    <div className={classes.content_container}>
      <form>
        <input
          type="file"
          name="myImage"
          onChange={(e) => {
            chooseFileImage(e)
          }}
        />
        <button onClick={submitImage}></button>
      </form>

      <header className={classes.content_header}>
        <span className={classes.content_header_text}>
          Наши товары
        </span>
      </header >
      <div className={classes.content_catalog}>
        {test_data_chapters.map((chapter) => 
          <Chapter products={props.products} name={chapter.name}/>
        )}
      </div>
    </div>
  );
}

export default Content;
