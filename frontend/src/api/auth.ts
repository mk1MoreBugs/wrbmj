import http from '@/api/http.ts';

import type { UserCredentials } from '@/models/UserCredentials';
import type { AuthResponse } from '@/models/ApiResponse';

export const authApi = {
  async login(credentials: UserCredentials): Promise<AuthResponse> {
    
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    console.log('FormData:', formData.toString());

    const { data } = await http.post<AuthResponse>('/auth/login', formData, {
       headers: {
         'Content-Type': 'application/x-www-form-urlencoded',
       },
     });

    return data;
  },
};
