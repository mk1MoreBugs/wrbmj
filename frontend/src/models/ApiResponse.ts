export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ErrorResponse {
  detail: string;
}