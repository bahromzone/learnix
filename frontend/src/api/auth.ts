import apiClient from './client';
import { ENDPOINTS } from '../config/api';
import { 
  LoginCredentials, 
  TokenResponse, 
  User, 
  CreateUserDto, 
  UpdateUserDto 
} from '../types';

export const authService = {
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await apiClient.post<TokenResponse>(ENDPOINTS.LOGIN, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
    if (response.role) {
      localStorage.setItem('user_role', response.role);
    }

    return response;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_role');
  },

  refreshToken: async (refreshToken: string): Promise<TokenResponse> => {
    return apiClient.post<TokenResponse>(ENDPOINTS.REFRESH_TOKEN, { refresh_token: refreshToken });
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },

  getToken: (): string | null => {
    return localStorage.getItem('access_token');
  },

  getUserRole: (): string | null => {
    return localStorage.getItem('user_role');
  },
};

export const userService = {
  getOwnProfile: async (): Promise<User> => {
    return apiClient.get<User>(ENDPOINTS.GET_OWN_PROFILE);
  },

  updateOwnProfile: async (data: UpdateUserDto): Promise<User> => {
    return apiClient.put<User>(ENDPOINTS.UPDATE_OWN_PROFILE, data);
  },

  uploadProfileImage: async (file: File): Promise<{ message: string }> => {
    return apiClient.uploadFile(ENDPOINTS.UPLOAD_USER_IMAGE, file);
  },

  deleteOwnAccount: async (): Promise<{ message: string }> => {
    return apiClient.delete(ENDPOINTS.DELETE_OWN);
  },

  // Admin functions
  getAllUsers: async (): Promise<User[]> => {
    return apiClient.get<User[]>(ENDPOINTS.GET_ALL_USERS);
  },

  getAllTeachers: async (): Promise<User[]> => {
    return apiClient.get<User[]>(ENDPOINTS.GET_ALL_TEACHERS);
  },

  getTeacherCount: async (): Promise<{ count: number }> => {
    return apiClient.get(ENDPOINTS.GET_TEACHER_COUNT);
  },

  createTeacher: async (data: CreateUserDto): Promise<User> => {
    return apiClient.post(ENDPOINTS.CREATE_TEACHER, data);
  },

  createAdmin: async (data: CreateUserDto): Promise<User> => {
    return apiClient.post(ENDPOINTS.CREATE_ADMIN, data);
  },

  createBoss: async (data: CreateUserDto): Promise<User> => {
    return apiClient.post(ENDPOINTS.CREATE_BOSS, data);
  },

  updateUser: async (id: number, data: UpdateUserDto): Promise<User> => {
    return apiClient.put(`${ENDPOINTS.UPDATE_USER}?ident=${id}`, data);
  },

  deleteUser: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_USER}?ident=${id}`);
  },

  deleteTeacher: async (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`${ENDPOINTS.DELETE_TEACHER}?ident=${id}`);
  },
};
