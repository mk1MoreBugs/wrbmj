import type { UserCredentials } from "@/models/UserCredentials.ts"

export interface UserRegistrationStoreModel extends UserCredentials {
  photoFile: string | null,
  repeatPassword: string
}

export interface UserRegistrationApiModel {
  username: string,
  plain_password: string,
  photo_file: string
}
