/* eslint-disable camelcase */
/* eslint-disable react/prop-types */
import React, { useEffect, useState, useRef } from "react"
import { FaUserFriends } from "react-icons/fa"
import { useStoreon } from "storeon/react"
import style from "./ChatPage.module.css"
import { Header } from "../../components/Header/Header"
import Chat from "../../components/Chat/Chat"
import Message from "../../components/Message/Message"
import Input from "../../components/Input/Input"
import { navigate } from "../../store"
import useApi from "../../Hooks/useApi"
import Popup from "../../components/Popup/Popup"
import useIsImage from "../../Hooks/useIsImage"
import { formatDuration, set } from "date-fns"
import SearchBar from "../../components/SearchBar/SearchBar"
import LoadButton from "../../components/LoadButton/LoadButton"

const ChatPage = () => {
  const { user } = useStoreon("user")
  const apiCreateConversations = useApi()
  const apiLastChats = useApi()
  const apiFiveLastConversations = useApi()
  const apiMessages = useApi()
  const apiSendMessage = useApi()
  const apiImageMine = useApi()
  const isImage = useIsImage()

  const [currentChat, setCurrentChat] = useState("")
  const [fiveMoreConversations, setfiveMoreConversations] = useState(5) // despues cambiar esto.
  const [textMessage, setTextMessage] = useState("")
  const [idCurrentChat, setIdCurrentChat] = useState()
  const [warning, setWarning] = useState(false)
  const [error, setError] = useState("")
  const [typePopUp, setTypePopUp] = useState(1)
  const chatContainerRef = useRef(null)
  const [cambioChats, setCambioChats] = useState([])
  const [apiResponse, setApiResponse] = useState([])
  const [apiMessagesData, setApiMessagesData] = useState([])
  const [idUsuario2, setIdUsuario2] = useState("")
  const [pfpMine, setPfpMine] = useState("/images/pfp.svg")

  const obtainFiveMoreConversations = async () => {
    const response = await apiFiveLastConversations.retrieveConversationsLimit(
      user,
      fiveMoreConversations
    )
    if (response.status === 200) {
      setfiveMoreConversations(fiveMoreConversations + 5)
      setApiResponse(response.conversations)
    } else {
      setError("No se pudieron obtener más conversaciones")
      setWarning(true)
      setTypePopUp(1)
    }
  }

  const obtainMessages = async () => {
    if (currentChat !== "") {
      const response = await apiMessages.handleRequest(
        "POST",
        "/messages/retrieve",
        {
          conversation_id: idCurrentChat,
        }
      )
      if (response.status === 200) {
        setApiMessagesData(response.messages)
      }
    }
  }

  useEffect(() => {
    obtainMessages()
    if (currentChat !== "") {
      const intervalMensajesChatActual = setInterval(() => {
        obtainMessages()
      }, 5000)
      return () => clearInterval(intervalMensajesChatActual)
    }
  }, [currentChat])

  const scrollDown = () => {
    chatContainerRef.current.scrollTo({
      top: chatContainerRef.current.scrollHeight,
      behavior: "smooth",
    })
  }

  const obtainImageFunc = async () => {
    const img = await apiImageMine.obtainImage("users/profilepic", {
      id: user,
    })
    setPfpMine(img)
  }

  useEffect(() => {
    scrollDown()
  }, [cambioChats])

  useEffect(() => {
    obtainFiveMoreConversations()
    obtainImageFunc()
  }, [])

  const sendMessage = async () => {
    await apiSendMessage.handleRequest("POST", "/messages/", {
      id_conversacion: idCurrentChat,
      emisor: user,
      mensaje: textMessage,
      es_archivo: false,
    })
    scrollDown()
    obtainMessages()
  }

  const handleInputChange = (e) => {
    setTextMessage(e.target.value)
  }

  const handleSendMessage = () => {
    sendMessage()
    setTextMessage("")
  }

  // Estado para controlar la visibilidad del contenedor de chats
  const [showChats, setShowChats] = useState(false)

  // Función para alternar la visibilidad del contenedor de chats
  const toggleChats = () => {
    setShowChats(!showChats)
  }

  const handleChat = (receptor, id) => {
    setCurrentChat(receptor)
    setCambioChats(receptor)
    setIdCurrentChat(id)
    setShowChats(false)
  }

  const handleSearch = async () => {
    const response = await apiCreateConversations.handleRequest(
      "POST",
      "/conversations/",
      {
        id_usuario1: user, // this should be the user id of the current user (logged in)
        id_usuario2: idUsuario2,
      }
    )
    console.log(response)
    /*
    if (response.status !== 200){
      setError("No se pudo crear la conversación")
      setWarning(true)
      setTypePopUp(1)
    }
    */
    if (response.status === 200) {
      setError(response.message)
      setWarning(true)
      setTypePopUp(3)
    } else if (response.detail.status === 400) {
      setError(response.detail.message)
      setWarning(true)
      setTypePopUp(1)
    } else {
      setError(response.detail.message)
      setWarning(true)
      setTypePopUp(1)
    }
  }

  const handleValue = (e) => {
    setIdUsuario2(e.target.value)
  }

  return (
    <div className={style.container}>
      <Header userperson="student" />
      <Popup
        message={error}
        status={warning}
        style={typePopUp}
        close={() => setWarning(false)}
      />
      <button type="button" className={style.menuButton} onClick={toggleChats}>
        <FaUserFriends size={30} color="#000" />
      </button>
      <div className={style.generalChatContainer}>
        <div className={style.leftContainer}>
          <div
            className={`${style.chatsContainer} ${
              showChats ? style.showChat : style.hideChat
            }`}
          >
            {apiResponse && apiResponse.length > 0 ? (
              apiResponse.map((chat) => (
                <Chat
                  pfp="/images/pfp.svg"
                  name={chat.nombre_persona}
                  lastChat={
                    chat.contenido_ultimo_mensaje === ""
                      ? `Inicia una conversación con ${chat.nombre_persona}`
                      : chat.contenido_ultimo_mensaje
                  }
                  key={chat.id_conversacion.toString()}
                  id_postulacion={chat.id_conversacion.toString()}
                  onClick={() =>
                    handleChat(chat.nombre_persona, chat.id_conversacion)
                  }
                />
              ))
            ) : (
              <div className={style.noUsersMessage}>
                No tienes conversaciones
              </div>
            )}

            <LoadButton
              onClick={obtainFiveMoreConversations}
              text="Cargar más"
            />
          </div>
          <div className={style.searchBarContainer}>
            <SearchBar search={handleSearch} onChange={handleValue} />
          </div>
        </div>
        <div
          className={`${style.currentChatContainer} ${
            showChats ? style.hide : style.show
          }`}
          ref={chatContainerRef}
        >
          {apiMessagesData && apiMessagesData.length > 0 ? (
            apiMessagesData.map((message, number) => {
              const side = message.id_emisor === user ? "right" : "left"
              //const side = message.emisor === user ? "right" : "left"
              number += 1
              const pfpUrlEmisor =
                side === "right" ? pfpMine : "/images/pfp.svg"
              return (
                <Message
                  key={[message.emisor, number]}
                  pfp={pfpUrlEmisor}
                  name={message.emisor}
                  time={message.fechahora}
                  message={message.mensaje}
                  file={""}
                  side={side}
                />
              )
            })
          ) : (
            <div className={style.noMessagesMessage}>No tienes mensajes</div>
          )}
          <div className={style.inputContainer}>
            <div className={style.inputBar}>
              <Input
                name="message"
                type="text"
                value={textMessage}
                placeholder="Escribe un mensaje..."
                onChange={handleInputChange}
              />
            </div>
            <div className={style.buttonSend}>
              <button
                type="button"
                className={style.button}
                style={{
                  backgroundColor:
                    textMessage === "" || currentChat === ""
                      ? "#D6CFF2"
                      : "#9c8bdf",
                }}
                disabled={textMessage === "" || currentChat === ""}
                onClick={handleSendMessage}
              >
                <img src="/images/send.svg" alt="send" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatPage
