import { useState } from 'react';
import classes from './Carusel.module.css';
import Container from './Container/Container';
import ButtonSwitch from './ButtonSwitch/ButtonSwitch';

const images = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'gray']
const componentImages = [images[images.length - 1], images[0],images[1],images[2]]

function Carusel(props) {

  
  const [idImage, setIdImage] = useState(0); //id центрального цвета
  const [idPropert, setidPropert] = useState(0); //прибавление к пропертсам
  const [idCompCurrHidden, setIdCompCurrHidden] = useState(3); //показывает, id какого из comimages скрыт

  const width = 150;
  const height = 300;
  const properties = [
    {
      width: width * 0.8,
      height: height * 0.8,
      left: -300,
      zIndex: 7,
      opacity: 0.6
    },
    {
      width: width,
      height: height,
      left: 0,
      zIndex: 8,
      opacity: 1
    },
    {
      width: width* 0.8,
      height: height* 0.8,
      left: 300,
      zIndex: 7,
      opacity: 0.6
    },
    {
      width: width* 0.4,
      height: height* 0.4,
      left: 0,
      zIndex: 6,
      opacity: 0
    },
  ]

  const getidPropert = (num) => {
    if (idPropert + num >= properties.length) {
      return idPropert + num - properties.length
    } else {
      return idPropert + num
    }
  }
  

  const onClickLeftButton = () => {
    if (idImage === images.length - 2) {
      componentImages[idCompCurrHidden] = images[0]
    } else if (idImage === images.length - 1) {
      componentImages[idCompCurrHidden] = images[1]
    } else {
      componentImages[idCompCurrHidden] = images[idImage + 2]
    }
    
    if (idImage === images.length - 1) {
      setIdImage(0)
    } else {
      setIdImage(idImage + 1)
    }

    if (idPropert === 0) {
      setidPropert(componentImages.length - 1)
    } else {
      setidPropert(idPropert - 1)
    }
    
    
    if (idCompCurrHidden === componentImages.length - 1) {
      setIdCompCurrHidden(0)
    } else {
      setIdCompCurrHidden(idCompCurrHidden + 1)
    }
  }

  const onClickRightButton = () => {

    if (idImage === 0) {
      componentImages[idCompCurrHidden] = images[images.length - 2]
    } else if (idImage === 1) {
      componentImages[idCompCurrHidden] = images[images.length - 1]
    } else {
      componentImages[idCompCurrHidden] = images[idImage - 2]
    }
    
    if (idImage === 0) {
      setIdImage(images.length - 1)
    } else {
      setIdImage(idImage - 1)
    }

    if (idPropert === componentImages.length - 1) {
      setidPropert(0)
    } else {
      setidPropert(idPropert + 1)
    }
    
    
    if (idCompCurrHidden === 0) {
      setIdCompCurrHidden(componentImages.length - 1)
    } else {
      setIdCompCurrHidden(idCompCurrHidden - 1)
    }
    setTimeout(1000)
  }

  return (
    <div className={classes.carusel}>
      <div className={classes.buttonSwitch + " " + classes.goLeftBut}><ButtonSwitch onClick={onClickLeftButton}/></div>
      <div className={classes.buttonSwitch + " " + classes.goRightBut}><ButtonSwitch onClick={onClickRightButton}/></div>
      <Container properties={properties[getidPropert(0)]} color={componentImages[0]}/>
      <Container properties={properties[getidPropert(1)]} color={componentImages[1]}/>
      <Container properties={properties[getidPropert(2)]} color={componentImages[2]}/>
      <Container properties={properties[getidPropert(3)]} color={componentImages[3]}/>
    </div>
  );
}

export default Carusel;
