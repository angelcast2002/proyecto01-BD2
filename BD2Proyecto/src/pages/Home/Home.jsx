import React from "react"
import style from "./Home.module.css"
import Message from "../../components/Message/Message"
import image1 from "/images/personExample1.jpg"
import image2 from "/images/personExample2.jpg"
import Button from "../../components/Button/Button"
import { navigate } from "../../store"

const Home = () => {
  const logIn = () => {
    navigate("login")
  }
  const signUp = () => {
    navigate("signup")
  }

  return (
    <div className={style.mainContainer}>
      <div className={style.leftContainer}>
        <div className={style.aboutUs}>
          <h1>Chatea con nosotros</h1>
          <p>
            Inicia sesión para chatear con usuarios o crea gratis una cuenta
            para empezar a chatear con otros usuarios.
          </p>
        </div>
        <div className={style.buttons}>
            <Button text="Iniciar sesión" size="250px" onClick={logIn}/>
            <Button text="Crear cuenta" size="250px" onClick={signUp}/>
            <Button text="Nuestros datos" size="250px" onClick={() => navigate("charts")}/>
        </div>
      </div>
      <div className={style.rightContainer}>
        <div className={style.imgExample}>
          <div className={style.messages}>
            <Message
              pfp={image1}
              name="Juan"
              message="Hola que tal?"
              side="right"
              nameColor="#000"
            />
            <Message
              pfp={image2}
              name="Karen"
              message="Bien y tu?"
              side="left"
              nameColor="#000"
            />
            <Message
              pfp={image1}
              name="Juan"
              message="Sale party o que?"
              side="right"
              nameColor="#000"
            />
            <Message
              pfp={image2}
              name="Karen"
              message="SIIII!!!"
              side="left"
              nameColor="#000"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
