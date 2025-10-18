import { ref, computed } from "vue"
import { defineStore } from "pinia"
import { reactive } from "vue"

import { authApi } from '@/api/auth.ts'
import type { UserCredentials } from "@/models/UserCredentials.ts"
import type { AuthResponse, ErrorResponse } from '@/models/ApiResponse'
import type { AxiosError } from 'axios';

export const useAuthStore = defineStore("auth", () => {
  const passwordError = ref('')
  const loginError = ref('')
  const userCredentials = reactive<UserCredentials>({ username: "", password: "" })

  const token = ref<string | null>(localStorage.getItem('token') || null)

  const isFormValid = computed(() => {
      let formIsCorrect: boolean = true

    if (userCredentials.username.length < 3) {
        loginError.value = 'username < 3'
        formIsCorrect = false
    }
    if (userCredentials.password.length < 8) {
       passwordError.value = 'password < 8'
       formIsCorrect = false
    }
    return formIsCorrect
  })

  const handleUsernameInput = (value: string): void => {
    setLoginError('')
    userCredentials.username = value
  }

  const handlePasswordInput = (value: string): void => {
    setPasswordError('')
    userCredentials.password = value
}

 const setPasswordError = (value: string): void => {
    passwordError.value = value
  }

  const setLoginError = (value: string): void => {
    loginError.value = value
  }

  async function login(credentials: UserCredentials): Promise<AuthResponse> {
     try {
      const response = await authApi.login(credentials);
      token.value = response.access_token;
      localStorage.setItem('token', response.access_token);
      return response;

    } catch (error: unknown) {
      const axiosError = error as AxiosError<ErrorResponse>;

      console.log('Error status:', axiosError.response?.status);
      console.log('Error data:', axiosError.response?.data);

       if (axiosError.response?.status === 401) {
        const errorDetail = axiosError.response.data?.detail || 'Invalid credentials';
        throw new Error(errorDetail);
      }

      if (axiosError.response?.status) {
        throw new Error(`Login failed with status: ${axiosError.response.status}`);
      }

      throw new Error('Network error during login');
    }
  }

  function logout() {
      token.value = null;
      localStorage.removeItem('token');
  }

  return {
    // State
    userCredentials,
    passwordError,
    loginError,
    token,

    //Getters
    isFormValid,

    // Actions
    handleUsernameInput,
    handlePasswordInput,
    setPasswordError,
    setLoginError,
    login,
    logout
  }
})
