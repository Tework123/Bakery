import { useState } from 'react';
import classes from './ProductEditor.module.css';
import axios from 'axios';
import ProductCard from '../../Content/ProductCard/ProductCard'

function ProductEditor(props) {
  
  const [cards, setCards] = useState([])
  const [selectedImage, setSelectedImage] = useState(null);
  const [image, setImage] = useState(null)
  const [testImage, setTestImage] = useState('')

  const chooseFileImage = (e) => {
    setImage(URL.createObjectURL(e.target.files[0]))
    console.log(image);
    setSelectedImage(e.target.files[0])
    console.log(e.target.files[0]);
  }

  const submitImage = () => {
    const formData = new FormData();
    console.log(selectedImage);
    formData.append('image', selectedImage);
    formData.append('name', 'Имя карточки');
    formData.append('price', 999);
    axios.post('/restaurant/cards', formData).then((response) => {

      console.log('Пришло: ' + response);
      console.log(response)
    })
  }
  
  return (
    <div className={classes.editor_container}>
      <div className={classes.editor_edit}>
      <header className={classes.title}>Редактирование товара</header>
      <div className={classes.editor_input_field}>
        <div className={classes.editor_input_name}>Название</div>
        <input></input>
      </div>
      <div className={classes.editor_input_field}>
        <div className={classes.editor_input_name}>Описание</div>
        <input></input>
      </div>
      <div className={classes.editor_input_field}>
        <div className={classes.editor_input_name}>Цена</div>
        <input></input>
      </div>
      <form encType="multipart/form-data" >
        <input
          type="file"
          name="myImage"
          onChange={(e) => {
            chooseFileImage(e)
          }}
        />
        <button type='button' onClick={submitImage}>Отправить картинку</button>
      </form>
      <img alt="image from server not loaded" src={testImage}/>
      </div>
      <div className={classes.editor_preview}>
        <ProductCard product={''}/>
      </div>
    </div>
  );
}

export default ProductEditor;
