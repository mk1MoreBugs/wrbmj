import type { UserCredentials } from "@/models/UserCredentials.ts"

export interface UserRegistration extends UserCredentials {
  photoFile: string | null
}
