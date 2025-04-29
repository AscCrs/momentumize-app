import { useState } from 'react'
import './styles/App.css'

function App() {
  return (
    <>
      <h1>Bienvenido <span className="user">Usuario</span></h1>
      <h2>A <span className="title">momentumize</span>, tu ayuda al seguimiento de rutinas</h2>
      <div className="card">
        <h3>Iniciar Sesión</h3>
        <div className="data">
          <label htmlFor="email">Email</label>
          <input type="email"/>
        </div>
        <button onClick={() => console.log("Login")}>
          Login
        </button>
        <p>
          If you are not registered, please register.
        </p>
      </div>
      <footer className="footer">
        By <code className='user'>AscCrs</code> Web Developer since <code>2020</code>
      </footer>
    </>
  )
}

export default App
