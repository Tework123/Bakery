import { useEffect, useState } from 'react';
import axios from 'axios'
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);
  const [login, setLogin] = useState("");
  const [register, setRegister] = useState("");


  useEffect(() => {
    axios.get("/main/").then((response) => {
      setCurrentTime(response.data.data);
    });
  }, []);

  const changeLogin = (e) => {
    console.log(e.target.value);
    setLogin(e.target.value)
  }

  const changeRegister = (e) => {
    console.log(e.target.value);
    setRegister(e.target.value)
  }

  function sendLogin() {
    axios.post('/main/login', {login: login}).then((response) => {console.log(response.data.data)})

  }

    function sendRegister() {
    axios.post('/main/register', {register: register}).then((response) => {console.log(response.data.data)})

  }


  return (
    <div className="App">
      <header className="App-header">
        <input placeholder='Регистрация' onChange={changeRegister} value={register}></input>

        <button onClick={sendRegister}>Зарегистрироваться</button>

        <p>The current time is {currentTime}.</p>



        <input placeholder='Логин' onChange={changeLogin} value={login}></input>
        <button onClick={sendLogin}>Авторизоваться</button>

      </header>
    </div>


  );
}

export default App;
