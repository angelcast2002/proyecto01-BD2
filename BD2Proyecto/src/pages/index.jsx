import { useStoreon } from "storeon/react"
import { routerKey } from "@storeon/router"
import React from "react"
import Home from "./Home/Home"
import LogIn from "./LogIn/LogIn"
import SignUp from "./SignUp/SignUp"
import Chat from "./ChatPage/ChatPage"
import EditProfile from "./EditProfile/EditProfile"
import ChartsPage from "./Charts/ChartsPage"

const Page = () => {
    const { [routerKey]: route } = useStoreon(routerKey)
  
    let Component = null
    switch (route.match.page) {
      case "home":
        Component = <Home />
        break // ver index en uniempleos para mas documentacion
      case "login":
        Component = <LogIn />
        break
      case "signup":
        Component = <SignUp />
        break
      case "chat":
        Component = <Chat />
        break
      case "editprofile":
        Component = <EditProfile />
        break
      case "charts":
        Component = <ChartsPage />
        break
      default:
        Component = <h1>404 Error</h1>
    }
  
    return <main>{Component}</main>
  }
  
  export default Page