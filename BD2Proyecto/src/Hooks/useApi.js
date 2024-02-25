import { useState } from "react"
import { useStoreon } from "storeon/react"
import API_URL from "../api"

const useApi = () => {
  const { user } = useStoreon("user")

  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleRequest = async (method, path, body = null) => {
    const options = {
      method,
      headers: {
        "Content-Type": "application/json",
      },
    }
    if (method === "POST" || method === "PUT") {
      options.body = JSON.stringify(body)
    }
    
    // console.info("API CALLL:", `${API_URL}/api${path}`, options)
    setLoading(true)
    const response = await fetch(`${API_URL}/api${path}`, options)
    const datos = await response.json() // Recibidos
    console.log("API RESPONSE:", datos)
    setLoading(false)
    setData(datos.data)

    if (datos.status !== 200) {
      setError(datos.message)
    }

    return datos
  }

  const updateProfilePicture = async (file) => {
    const formData = new FormData()
    formData.append("file", file)

    setLoading(true)
    const apiResponse = await fetch(`${API_URL}/api/users/upload`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${user.token}`,
      },
      body: formData,
    })
    const datos = await apiResponse.json()
    setLoading(false)
    setData(datos.data)

    if (datos.status !== 200) {
      setError(datos.message)
    }

    return datos
  }

  const createUser = async (name, lastName, mail, password, birthdate, file) => {
    const formData = new FormData()
    formData.append("id", mail)
    formData.append("password", password)
    formData.append("nombre", name)
    formData.append("apellido", lastName)
    formData.append("birthdate", birthdate)
    formData.append("profile_pic", file)

    setLoading(true)
    const apiResponse = await fetch(`${API_URL}/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: formData,
    })
    const datos = await apiResponse.json()
    setLoading(false)
    setData(datos.data)

    if (datos.status !== 200) {
      setError(datos.message)
    }

    return datos
  }

  return {
    error,
    user,
    data,
    loading,
    handleRequest,
    updateProfilePicture,
    createUser,
  }
}

export default useApi
