import classes from './Container.module.css';

function Container(props) {

  return (
    <div
      className={classes.container}
      style={{
        position: 'absolute',
        backgroundColor: props.color,
        left: props.properties.left,
        width: props.properties.width,
        height: props.properties.height,
        zIndex: props.properties.zIndex,
        opacity: props.properties.opacity,
        right: 0,
        top: 0,
        bottom: 0,
        margin: 'auto',
        transition: 'all 0.5s'
        }}>
      
    </div>
  );
}

export default Container;
