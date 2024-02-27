import { useState } from "react"
import { useStoreon } from "storeon/react"
import API_URL from "../api"

const useApi = () => {
  const { user } = useStoreon("user")

  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleRequest = async (method, path, body = null, header1_1 = "Content-Type", header1_2 = "application/json") => {
    const options = {
      method,
      headers: {
        [header1_1]: header1_2,
        "Content-Type": "application/json",
      },
    }
    if (method === "POST" || method === "PUT") {
      options.body = JSON.stringify(body)
    }
    
    // console.info("API CALLL:", `${API_URL}/api${path}`, options)
    setLoading(true)
    const response = await fetch(`${API_URL}${path}`, options)
    const datos = await response.json() // Recibidos
    setLoading(false)
    setData(datos.user_info)

    if (datos.status !== 200) {
      setError(datos.message)
    }

    return datos
  }

  const retrieveConversationsLimit = async (id_user, limit) => {
    setLoading(true)
    // /conversations/retrieve/limit/
    // user_id: id_user, limit: limit
    // POST
    const apiResponse = await fetch(`${API_URL}/conversations/retrieve/limit/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_id: id_user, limit: limit }),
    })

    const datos = await apiResponse.json()
    setLoading(false)
    setData(datos.data)

    if (datos.status !== 200) {
      setError(datos.message)
    }

    return datos
  }

  const updateProfilePicture = async (file, path) => {
    const formData = new FormData()
    formData.append("profile_pic", file)
    setLoading(true)
    const apiResponse = await fetch(`${API_URL}/${path}`, {
      method: "PUT",
      headers: {
        "accept": "application/json",
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

  const createUser = async (file, path) => {
    const formData = new FormData()
    formData.append("profile_pic", file)
    setLoading(true)
    const apiResponse = await fetch(`${API_URL}/users?${path}`, {
      method: "POST",
      headers: {
        "accept": "application/json",
      },
      body: formData,
    })
    const datos = await apiResponse.json()
    console.log("API RESPONSE:", datos)
    setLoading(false)
    setData(datos.data)

    if (datos.status !== 200) {
      setError(datos.message)
    }

    return datos
  }

  const editUser = async (path, type) => {
    console.log("Path", path)
    setLoading(true)
    const apiResponse = await fetch(`${API_URL}/users?${path}`, {
      method: type,
      headers: {
        "accept": "application/json",
      },
    })
    const datos = await apiResponse.json()
    console.log("API RESPONSE:", datos)
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
    editUser,
  }
}

export default useApi
