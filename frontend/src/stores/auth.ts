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
    userCredentials.username = value
  }

  const handlePasswordInput = (newValue: string) => {
  userCredentials.password = newValue;
}

  function login() {
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
    login 
  }
})