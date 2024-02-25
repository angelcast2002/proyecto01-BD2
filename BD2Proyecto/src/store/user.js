const user = (store) => {
    store.on("@init", () => ({
      user: {
        id_user: " ",
      },
    }))
    store.on("user/config", (_, newConfigs) => ({ user: newConfigs }))
  }
  
  export default user