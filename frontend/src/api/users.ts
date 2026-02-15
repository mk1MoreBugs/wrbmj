import http from "@/api/http.ts"

import type { UserRegistration } from "@/models/UserRegistration"
import type { AuthResponse } from "@/models/ApiResponse"

export const usersApi = {
  async registration(registrationData: UserRegistration): Promise<AuthResponse> {
    const { data } = await http
      .post<AuthResponse>("/users/create", registrationData, {
        headers: {
          "Content-Type": "application/json",
        },
      })
    return data
  },
}
