import { createRouter } from "@storeon/router"

export default createRouter([
	// ejemplo de rutas
  ["/", () => ({ page: "home" })],
  ["/login", () => ({ page: "login" })],
  ["/signup", () => ({ page: "signup" })],
  ["/chat", () => ({ page: "chat" })],
  ["/editprofile", () => ({ page: "editprofile" })],
  
  /*
	Ejemplo de rutas con promps y parametros
  ["/postulacion/*", (id) => ({ page: "postulacion", props: { id } })],
  ["/newoffer", () => ({ page: "newoffer" })],
  [
    "/adminSPDS/*",
    (param) => ({
      page: "adminShowPostulationDetailsStudent",
      props: { param },
    }),
  ],*/

])
