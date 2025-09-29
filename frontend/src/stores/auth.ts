import { ref, computed } from "vue"
import { defineStore } from "pinia"


export const useAuthStore = defineStore("auth", () => {
  const loginField = ref<string>('')
  const passwordField = ref<string>('')

  const isFormValid = computed<boolean>(() => {
    
    return loginField.value.length > 0 && passwordField.value.length > 8 // && todo
  })

  const setLoginField = (value: string): void => {
    loginField.value = value
  }

  const setPasswordField = (value: string): void => {
    passwordField.value = value
  }

  function login() {
    //todo
  }

  return {
    // State
     loginField, passwordField,
     
     //Getters
     isFormValid,

     // Actions
     setLoginField,
    setPasswordField,
    login 
  }
})