import { useState } from 'react';
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

  const [selectedImage, setSelectedImage] = useState(null);


  const chooseFileImage = (e) => {
    setSelectedImage(e.target.files[0])
    console.log(e.target.files[0]);
    axios.post('/admin/cards', { post:  e.target.files[0]}).then((response) => {
    console.log(response.data.data)

    })
  }

  return (
    <div className={classes.content_container}>

{/* {       <img
            alt="not found"
            width={"250px"}
            src={URL.createObjectURL(selectedImage)}
        />} */}

    <input

        type="file"
        name="card_image"
        onChange={(e) => {
          chooseFileImage(e.target.files[0])
          axios.post('/admin/cards', { post: selectedImage }).then((response) => {
            console.log(response.data.data)

          })
        }}
      />
  

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
