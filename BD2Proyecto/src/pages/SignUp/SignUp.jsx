import React, { useEffect, useState } from "react"
import style from "./SignUp.module.css"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import { navigate } from "../../store"
import { useStoreon } from "storeon/react"
import InputFile from "../../components/InputFile/InputFile"
import { AiOutlineCloudDownload } from "react-icons/ai"
import { TbEdit } from "react-icons/tb"
import Loader from "../../components/Loader/Loader"

// pedir correo, password, nombre, apellido, pfp
const SignUp = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [pfp, setPfp] = useState("")
  const [pfpPreview, setPfpPreview] = useState("/images/pfp.svg")
  const [pfpText, setPfpText] = useState("")
  
  const [passWord, setPassWord] = useState("")
  const [email, setEmail] = useState("")
  const [nombres, setNombres] = useState("")
  const [apellidos, setApellidos] = useState("")

  const handleImageSelect = (event) => {
    const selectedFile = event.target.files[0]
    if (
      selectedFile &&
      (selectedFile.type === "image/png" ||
        selectedFile.type === "image/jpeg" ||
        selectedFile.type === "image/jpg")
    ) {
      setPfpText(selectedFile.name)
      setPfp(selectedFile)
      setPfpPreview(URL.createObjectURL(selectedFile))
    }
  }

  const handlePassword = () => {
    setShowPassword(!showPassword)
  }

  const handleSignUp = () => {}

  const handleInputsValue = (e) => { 
    switch (e.target.name) {
      case "correo":
        setEmail(e.target.value)
        break
      case "password":
        setPassWord(e.target.value)
        break
      case "nombres":
        setNombres(e.target.value)
        break
      case "apellidos":
        setApellidos(e.target.value)
        break
      default:
        break
    }
  }

  return (
    <div className={style.signUpCointainer}>
      {isLoading ? (
        <div className={style.loaderContainer}>
          <Loader size={100} />
        </div>
      ) : (
        <div className={style.mainContainer}>
          <div className={style.imgContainer}>
            <img src={pfpPreview} alt="profile picture" />
            <div className={style.editImageContainer}>
              <label>
                <TbEdit size={25} color="#fff" className={style.imageSvg} />
                <input
                  type="file"
                  accept=".jpg, .jpeg, .png"
                  className={style.inputImage}
                  style={{ display: "none" }}
                  onChange={handleImageSelect}
                />
              </label>
            </div>
          </div>
          <div className={style.dataContainer}>
            <div className={style.dataGroup1Container}>
              <div className={style.nameContainer}>
                <span>Nombre</span>
                <ComponentInput
                  name="nombres"
                  type="text"
                  placeholder="Esteban"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.lastNameContainer}>
                <span>Apellido</span>
                <ComponentInput
                  name="apellidos"
                  type="text"
                  placeholder="Nano"
                  onChange={handleInputsValue}
                />
              </div>
            </div>
            <div className={style.dataGroup2Container}>
              <div className={style.emailContainer}>
                <span>Correo</span>
                <ComponentInput
                  name="correo"
                  type="text"
                  placeholder="uni@uni.com"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.passwordContainer}>
                <span>Contraseña</span>
                <ComponentInput
                  name="password"
                  type="password"
                  placeholder="micontraseña123"
                  onChange={handleInputsValue}
                  eye
                  onClickButton={handlePassword}
                  isOpen={showPassword}
                />
              </div>
            </div>
            <div className={style.buttonContainer}>
              <Button text="Crear cuenta" onClick={handleSignUp} size={"75%"} />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SignUp
