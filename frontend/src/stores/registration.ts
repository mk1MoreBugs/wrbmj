import { ref, computed } from "vue"
import { defineStore } from "pinia"
import { reactive } from "vue"

import { usersApi } from "@/api/users.ts"
import { fileToBase64 } from "@/utils/fileToBase64.ts"

import type { UserRegistrationApiModel, UserRegistrationStoreModel } from "@/models/UserRegistration"
import type { AuthResponse, ErrorResponse } from "@/models/ApiResponse"
import type { AxiosError } from "axios"


export const useRegistrationStore = defineStore("registration", () => {
  const passwordError = ref("")
  const loginError = ref("")
  const photoError = ref("")

  const userRegistration = reactive<UserRegistrationStoreModel>({
    username: "",
    password: "",
    repeatPassword: "",
    photoFile: "1111",
  })

  // TODO: Вынести в отдельный метод
  const isFormValid = computed(() => {
    let formIsCorrect: boolean = true

    if (userRegistration.username.length < 3) {
      loginError.value = "username < 3"
      formIsCorrect = false
    }

    if (userRegistration.password.length < 8) {
      passwordError.value = "password < 8"
      formIsCorrect = false
    }

    if (userRegistration.password !== userRegistration.repeatPassword) {
      passwordError.value = "Пароли не совпадают"
      formIsCorrect = false
    }

    if (!userRegistration.photoFile) {
      photoError.value = "Фото обязательно"
      formIsCorrect = false
    }

    return formIsCorrect
  })

  const handleUsernameInput = (value: string): void => {
    setLoginError("")
    setPhotoError("")
    userRegistration.username = value
  }

  const handlePasswordInput = (value: string): void => {
    setPasswordError("")
    setPhotoError("")
    userRegistration.password = value
  }

  const handleRepeatPasswordInput = (value: string): void => {
    setPasswordError("")
    setPhotoError("")
    userRegistration.repeatPassword = value
  }

  const handlePhotoUpload = async (file: File) => {
    try {
      if (!file.type.startsWith("image/")) {
        throw new Error("Только изображения")
      }
      if (file.size > 5 * 1024 * 1024) {
        // 5 MB
        throw new Error("Файл не более 5MB")
      }

      const base64 = await fileToBase64(file)

      userRegistration.photoFile = base64
      photoError.value = ""
    } catch (error: unknown) {
      if (error instanceof Error) {
        photoError.value = error.message
      } else {
        photoError.value = String(error)
      }
    }
  }

  const resetPhoto = () => {
    userRegistration.photoFile = null
    photoError.value = ""
  }

  const setPasswordError = (value: string): void => {
    passwordError.value = value
  }

  const setLoginError = (value: string): void => {
    loginError.value = value
  }

  const setPhotoError = (value: string): void => {
    loginError.value = value
  }

  async function registration(registrationData: UserRegistrationApiModel): Promise<AuthResponse> {
    try {
      const response = await usersApi.registration(registrationData)
      localStorage.setItem("token", response.access_token)
      return response
    } catch (error: unknown) {
      const axiosError = error as AxiosError<ErrorResponse>

      console.log("Error status:", axiosError.response?.status)
      console.log("Error data:", axiosError.response?.data)

      if (axiosError.response?.status === 401) {
        const errorDetail = axiosError.response.data?.detail || "Invalid credentials"
        throw new Error(errorDetail)
      }

      if (axiosError.response?.status) {
        throw new Error(`Login failed with status: ${axiosError.response.status}`)
      }

      throw new Error("Network error during login")
    }
  }

  return {
    // State
    userRegistration,
    passwordError,
    loginError,

    //Getters
    isFormValid,

    // Actions
    handleUsernameInput,
    handlePasswordInput,
    handleRepeatPasswordInput,
    handlePhotoUpload,
    resetPhoto,
    setPasswordError,
    setLoginError,
    setPhotoError,
    registration,
  }
})
