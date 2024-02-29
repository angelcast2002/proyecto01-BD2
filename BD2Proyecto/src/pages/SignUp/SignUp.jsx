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
import useApi from "../../Hooks/useApi"
import { set } from "date-fns"
import Popup from "../../components/Popup/Popup"
import Switch from "../../components/Switch/Switch"

// pedir correo, password, nombre, apellido, pfp
const SignUp = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [pfp, setPfp] = useState("")
  const [pfpPreview, setPfpPreview] = useState("/images/pfp.svg")
  const [pfpText, setPfpText] = useState("")
  const { dispatch } = useStoreon("user")
  const api = useApi()

  const [passWord, setPassWord] = useState("")
  const [email, setEmail] = useState("")
  const [nombres, setNombres] = useState("")
  const [apellidos, setApellidos] = useState("")
  const [fechaNacimiento, setFechaNacimiento] = useState("")
  const [genre, setGenre] = useState(false)

  const [warning, setWarning] = useState(false)
  const [error, setError] = useState("")
  const [typeError, setTypeError] = useState(1)

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

  const handleHome = () => {
    navigate("/")
  }

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
      case "fechaNacimiento":
        setFechaNacimiento(e.target.value)
        break
      default:
        break
    }
  }

  const handleSignUp = async () => {
    if (
      nombres === "" ||
      apellidos === "" ||
      email === "" ||
      passWord === "" ||
      fechaNacimiento === "" ||
      pfp === ""
    ) {
      setError("Todos los campos son obligatorios")
      setTypeError(2)
      setWarning(true)
    } else {
      const response = await api.createUser(
        pfp,
        `id=${email}&password=${passWord}&nombre=${nombres}&apellido=${apellidos}&birthdate=${fechaNacimiento}&gender=${genre}`
      )
      const data = response
      if (data.status === 200) {
        setIsLoading(true)
        setError("Cuenta creada exitosamente, redirigiendo...")
        setTypeError(3)
        setWarning(true)
        dispatch("user/config", email)
        setTimeout(() => {
          setIsLoading(false)
          navigate("/chat")
        }, 5000)
      } else if (data.status === 404) {
        setError(data.message)
        setTypeError(2)
        setWarning(true)
      } else {
        setError(response.detail.message)
        setTypeError(1)
        setWarning(true)
      }
      setIsLoading(false)
    }
  }

  const handleGenre = (e) => {
    setGenre(e.target.checked)
  }
  console.log(genre)

  return (
    <div className={style.signUpCointainer}>
      <Popup
        message={error}
        status={warning}
        style={typeError}
        close={() => setWarning(false)}
      />
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
              <div className={style.birthDateContainer}>
                <span>Fecha de nacimiento</span>
                <ComponentInput
                  name="fechaNacimiento"
                  type="date"
                  placeholder="2018-07-22"
                  min="1940-01-01"
                  max="2005-01-01"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.genreContainer}>
                <Switch 
                  value={genre}
                  onClick={handleGenre}
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
              <Button text="Regresar" onClick={handleHome} size={"75%"} />
              <Button text="Crear cuenta" onClick={handleSignUp} size={"75%"} />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SignUp
