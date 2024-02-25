import React, { useState, useEffect } from "react"
import { navigate } from "../../store"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import styles from "./LogIn.module.css"
import { useStoreon } from "storeon/react"
import useApi from "../../Hooks/useApi"
import Popup from "../../components/Popup/Popup"

const LogIn = () => {
  const [showPassword, setShowPassword] = useState(false)
  const [passWord, setPassWord] = useState("")
  const [email, setEmail] = useState("")
  const { dispatch } = useStoreon("user")
  const api = useApi()

  const [warning, setWarning] = useState(false)
  const [error, setError] = useState("")
  const [typeError, setTypeError] = useState(1)


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

  const handleLogIn = async () => {
    const response = await api.handleRequest("POST", "/login", {
      id: email,
      password: passWord,
    })

    console.log(response)

    if (response.status === 200) {
      dispatch("user/config", email)
      navigate("/home")
    } else {
      setError("Correo o contraseña incorrectos")
      setTypeError(2)
      setWarning(true)
    }
  }

  return (
    <div className={styles.logInCointainer}>
      < Popup 
        message={error}
        status={warning}
        style={typeError}
        close={() => setWarning(false)}
      />
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
          <Button text="Iniciar sesión" size={"75%"} onClick={handleLogIn}/>
        </div>
        <a href="/signup">
          Eres nuevo? <span> SingUp </span>
        </a>
      </div>
    </div>
  )
}

export default LogIn
