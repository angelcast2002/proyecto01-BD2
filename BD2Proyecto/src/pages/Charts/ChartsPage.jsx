import React from "react"
import style from "./ChartsPage.module.css"
import chartsJson from "./Charts.json"
import Charts from "../../components/Charts/Charts"
import { LuLogOut } from "react-icons/lu"
import { navigate } from "../../store"
import Button from "../../components/Button/Button"

const ChartsPage = () => {
  const logIn = () => {
    navigate("/login")
  }

  const signUp = () => {
    navigate("/signup")
  }

  return (
    <div className={style.mainContainer}>
      <div className={style.buttonLogoutMobile}>
        <Button text="Iniciar sesión" size="150px" onClick={logIn} />
        <Button text="Crear cuenta" size="150px" onClick={signUp} />
        <LuLogOut
          size={30}
          style={{ color: "#fff"}}
          onClick={() => {
            navigate("/")
          }}
        />
      </div>
      <div className={style.chartsContainer}>
        {chartsJson.map((chart, index) => {
          return (
            <div key={index} className={style.iFrameContainer}>
              <Charts key={index} src={chart.src} />
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default ChartsPage
