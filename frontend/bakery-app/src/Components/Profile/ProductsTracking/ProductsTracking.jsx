import { useEffect, useState } from 'react';
import classes from './ProductsTracking.module.css';
import axios from 'axios';

function ProductsTracking(props) {

  useEffect(() => {
    axios.get('/restaurant/cards').then((responce) => {
      console.log(responce.data);
    })
  }, [])
  
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
    <div className={classes.producttr_container}>
      <header className={classes.title}>Продукты</header>
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
      <div className={classes.producttr_search}>
        Search_лупа
      </div>
      <table className={classes.producttr_table}>
        <tr>
          <th>Название</th>
          <th>Категория</th>
          <th>ID</th>
        </tr>
        <tr>
          <td>Осетинский пирог</td>
          <td>Пироги</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Булочка с корицей</td>
          <td>Булочки</td>
          <td>2</td>
        </tr>
        <tr>
          <td>Булочка с маслом</td>
          <td>Булочки</td>
          <td>3</td>
        </tr>
        <tr>
          <td>Булочка с вишней</td>
          <td>Булочки</td>
          <td>4</td>
        </tr>
        <tr>
          <td>Комбо 2 в одном</td>
          <td>Комбо</td>
          <td>5</td>
        </tr>
        <tr>
          <td>Молочный коктейль</td>
          <td>Напитки</td>
          <td>6</td>
        </tr>
      </table>
    </div>
  );
}

export default ProductsTracking;
