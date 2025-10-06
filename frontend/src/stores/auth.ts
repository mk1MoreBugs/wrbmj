import { ref, computed } from "vue"
import { defineStore } from "pinia"
import { reactive } from "vue"
import type { UserCredentials } from "@/models/UserCredentials.ts"


export const useAuthStore = defineStore("auth", () => {
  const passwordError = ref('')
  const loginError = ref('')
  const userCredentials = reactive<UserCredentials>({ username: "", password: "" })

  const isFormValid = computed<boolean>(() => {
    
    return userCredentials.username.length > 0 && userCredentials.password.length > 8 // && todo
  })

  const handleUsernameInput = (value: string): void => {
    setLoginError('')
    userCredentials.username = value
  }

  const handlePasswordInput = (newValue: string) => {
    setPasswordError('')
    userCredentials.password = newValue
}

 const setPasswordError = (value: string): void => {
    passwordError.value = value
  }

  const setLoginError = (value: string): void => {
    passwordError.value = value
  }


  function login() {
    setPasswordError('true') //todo
    console.log(passwordError.value + loginError.value)
    console.log('login!') //todo
  }

  return {
    // State
     userCredentials,
     passwordError,
     loginError,
     
     //Getters
     isFormValid,

     // Actions
     handleUsernameInput,
    handlePasswordInput,
    setPasswordError,
    setLoginError,
    login
  }
})