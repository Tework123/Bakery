import classes from './ProductAddChange.module.css';

function ProductAddChange(props) {
  
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
    <div className={classes.productchange_container}>
      <div>
        <div>Название</div>
        <input></input>
      </div>
      <div>
        <div>Словесное описание</div>
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
  );
}

export default ProductAddChange;
