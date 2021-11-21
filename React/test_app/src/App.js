// import logo from './logo.svg';
import React, {useEffect} from 'react'
import './App.css';

function App() {

  useEffect(()=>{
    fetch("/summary?video link=https://www.youtube.com/watch?v=NhGNZXVy7cs&summary alg =T5").then(response =>
     console.log(response.body))},[])
  return (
    <div className="App">

    </div>
  );

}

export default App;
