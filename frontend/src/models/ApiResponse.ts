export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ErrorResponse {
  detail: string;
}

export interface NoteResponse {
  id: number,
  last_update: string,
  title_name: string,
  short_description: string,
}
