import { useEffect, useState } from 'react';
import axios from 'axios'
import './App.css';

function App() {
      const [currentTime, setCurrentTime] = useState(0);
  const [login, setLogin] = useState("");

  useEffect(() => {
    axios.get("/main/").then((response) => {
      setCurrentTime(response.data.data);
    });
  }, []);

  const changeLogin = (e) => {
    console.log(e.target.value);
    setLogin(e.target.value)
  }

  function sendLogin() {
    axios.post('/main/login', {login: login}).then((response) => {console.log(response.data.data)})

  }


  return (
    <div className="App">
      <header className="App-header">
        <input placeholder='Логин' onChange={changeLogin} value={login}></input>
        <button onClick={sendLogin}>Авторизоваться</button>

        <p>The current time is {currentTime}.</p>
      </header>
    </div>
  );
}

export default App;
