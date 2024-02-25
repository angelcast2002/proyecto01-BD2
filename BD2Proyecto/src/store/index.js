import { createStoreon } from "storeon"
import { storeonDevtools } from "storeon/devtools"
import { routerNavigate } from "@storeon/router"
import { persistState } from "@storeon/localstorage"
import router from "./router"

const store = createStoreon([
  router,
  storeonDevtools,
  persistState([])
])

const navigate = (target) => {
  store.dispatch(routerNavigate, target)
}

export { navigate }
export default store