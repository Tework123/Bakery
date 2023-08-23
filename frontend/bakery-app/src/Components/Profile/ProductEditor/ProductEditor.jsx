import { useEffect, useState } from 'react';
import classes from './ProductEditor.module.css';
import axios from 'axios';
import ProductCard from '../../Content/ProductCard/ProductCard'
import { useParams } from 'react-router-dom';

function ProductEditor(props) {
  
  const [selectedImage, setSelectedImage] = useState(null);
  const {card_id} = useParams()
  const [product, setProduct] = useState()

  if (card_id !== 'new') {
    axios.get(`/restaurant/cards/${card_id}`).then((response) => {
      product = response.data;
      console.log(response.data);
    })
  }
  

  const chooseFileImage = (e) => {
    setSelectedImage(URL.createObjectURL(e.target.files[0]))
    console.log(selectedImage);
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
      <div className={classes.editor_input_field + " " + classes.name}>
        <div className={classes.editor_input_name}>Название</div>
        <input></input>
      </div>
      <div className={classes.editor_input_field  + " " + classes.description}>
        <div className={classes.editor_input_name}>Описание</div>
        <input></input>
      </div>
      <div className={classes.editor_input_field + " " + classes.price}>
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
      </div>
      <div className={classes.editor_preview}>
        <ProductCard product={product} test={true}/>
      </div>
    </div>
  );
}

export default ProductEditor;
