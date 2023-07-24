import { useState } from 'react';
import classes from './Profile.module.css';
import axios from 'axios';


function Profile(props) {

  const [cards, setCards] = useState([])
  const [selectedImage, setSelectedImage] = useState(null);


  const chooseFileImage = (e) => {
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
      console.log(response)

    })
  }

  return (
    <div className={classes.profile_container}>
      <div className={classes.profile_user_information}>
        <div className={classes.profile_field_item}>
          <div className={classes.profile_field_text}>Имя</div>
          <input />
        </div>
      </div>
      <div className={classes.profile_order_history}>

      </div>
      <div>
        <form encType="multipart/form-data">
          <input
            type="file"
            name="myImage"
            onChange={(e) => {
              chooseFileImage(e)
            }}
          />
          <button onClick={submitImage}>Отправить картинку</button>
        </form>
      </div>
    </div>
  );
}

export default Profile;
