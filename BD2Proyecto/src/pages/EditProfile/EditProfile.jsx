import React, { useEffect, useState } from "react"
import style from "./EditProfile.module.css"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import { navigate } from "../../store"
import { useStoreon } from "storeon/react"
import { TbEdit } from "react-icons/tb"
import Loader from "../../components/Loader/Loader"
import useApi from "../../Hooks/useApi"
import Popup from "../../components/Popup/Popup"
import Header from "../../components/Header/Header"
import Switch from "../../components/Switch/Switch"

const EditProfile = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [pfp, setPfp] = useState("")
  const [pfpPreview, setPfpPreview] = useState("/images/pfp.svg")
  const [pfpText, setPfpText] = useState("")
  const { user } = useStoreon("user")
  const api = useApi()
  const apiUser = useApi()
  const apiDelete = useApi()

  const [nombres, setNombres] = useState("")
  const [apellidos, setApellidos] = useState("")
  const [fechaNacimiento, setFechaNacimiento] = useState("")

  const [warning, setWarning] = useState(false)
  const [error, setError] = useState("")
  const [typeError, setTypeError] = useState(1)

  const obtainData = async () => {
    await apiUser.handleRequest(
      "POST",
      "/users/info",
      {
        id: user,
      },
      "Accept"
    )
  }

  useEffect(() => {
    obtainData()
  }, [])

  useEffect(() => {
    if (apiUser.data) {
      setNombres(apiUser.data.nombre)
      setApellidos(apiUser.data.apellido)
      setFechaNacimiento(apiUser.data.birthdate)
      // La imagen no funcia
    }
  }, [apiUser.data])

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

  const handleEditInfo = async () => {
    if (nombres === "" || apellidos === "" || fechaNacimiento === "") {
      setError("Todos los campos son obligatorios")
      setTypeError(2)
      setWarning(true)
    } else {
      const response = await api.editUser(
        `id=${user}&nombre=${nombres}&apellido=${apellidos}&birthdate=${fechaNacimiento}`,
        "PUT"
      )
      const data = response
      if (data.status === 200) {
        setError("Cambios guardados con éxito")
        setTypeError(3)
        setWarning(true)
      } else if (data.status === 404) {
        setError(data.message)
        setTypeError(2)
        setWarning(true)
      } else {
        setError(response.detail.message)
        setTypeError(1)
        setWarning(true)
      }
      if (pfp !== "") {
        const response = await api.updateProfilePicture(
          pfp,
          `users/profilepic?user_id=${user}`
        )
        if (response.status === 200) {
          setTimeout(() => {
            setError("Imagen de perfil actualizada con éxito")
            setTypeError(3)
            setWarning(true)
          }, 5000)
        } else {
          setTimeout(() => {
            setError(response.message)
            setTypeError(1)
            setWarning(true)
          }, 5000)
        }
      }
    }
  }

  const handleDelete = async () => {
    const response = await apiDelete.handleRequest(
      "POST",
      "/users/delete",
      {
        id: user,
      },
      "Accept"
    )
    console.log("Response", response)
    const data = response.detail
    console.log("Data", data)
    if (response.status === 200) {
      setError(response.message)
      setTypeError(3)
      setWarning(true)
      setTimeout(() => {
        setIsLoading(false)
        navigate("/")
      }, 5000)
    } else {
      setError(data.message)
      setTypeError(1)
      setWarning(true)
    }
  }

  return (
    <div className={style.signUpCointainer}>
      <Header />
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
                  value={nombres}
                  type="text"
                  placeholder="Esteban"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.lastNameContainer}>
                <span>Apellido</span>
                <ComponentInput
                  value={apellidos}
                  name="apellidos"
                  type="text"
                  placeholder="Nano"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.birthDateContainer}>
                <span>Fecha de nacimiento</span>
                <ComponentInput
                  value={fechaNacimiento}
                  name="fechaNacimiento"
                  type="date"
                  placeholder="2018-07-22"
                  min="1940-01-01"
                  max="2005-01-01"
                  onChange={handleInputsValue}
                />
              </div>
            </div>
            <div className={style.buttonContainer}>
              <Button text="Eliminar" onClick={handleDelete} size={"75%"} />
              <Button
                text="Guardar cambios"
                onClick={handleEditInfo}
                size={"75%"}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default EditProfile
