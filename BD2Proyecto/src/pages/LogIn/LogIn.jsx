import React, { useState, useEffect } from "react"
import { navigate } from "../../store"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import styles from "./LogIn.module.css"
import { useStoreon } from "storeon/react"

const LogIn = () => {
  const [showPassword, setShowPassword] = useState(false)
  const [passWord, setPassWord] = useState("")
  const [email, setEmail] = useState("")


  const openEye = () => {
    console.log("click")
    setShowPassword(!showPassword)
  }

  const handleEmail = (e) => {
    setEmail(e.target.value)
  }

  const handlePassword = (e) => {
    setPassWord(e.target.value)
  }

  return (
    <div className={styles.logInCointainer}>
      <h1>ChaChat</h1>
      <div className={styles.inputsContainer}>
        <div className={styles.usuarioContainer}>
          <span>Correo</span>
          <ComponentInput
            name="correo"
            type="text"
            placeholder="chaChat@gmail.com"
            onChange={(e) => {
              handleEmail(e)
            }}
          />
        </div>
        <div className={styles.usuarioContainer}>
          <span>Contraseña</span>
          <ComponentInput
            name="password"
            type="password"
            placeholder="micontraseña123"
            eye
            isOpen={showPassword}
            onChange={(e) => {
              handlePassword(e)
            }}
            onClickButton={openEye}
          />
        </div>
        <div className={styles.buttonContainer}>
          <Button text="Iniciar sesión" size={"75%"}/>
        </div>
        <a href="/signup">
          Eres nuevo? <span> SingUp </span>
        </a>
      </div>
    </div>
  )
}

export default LogIn
