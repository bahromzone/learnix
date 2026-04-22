import { create } from 'zustand';
import { User } from '../types';
import { authService, userService } from '../api/auth';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  fetchProfile: () => Promise<void>;
  updateUser: (data: any) => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: authService.isAuthenticated(),
  isLoading: false,

  login: async (username: string, password: string) => {
    set({ isLoading: true });
    try {
      await authService.login({ username, password });
      await get().fetchProfile();
      set({ isAuthenticated: true, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  logout: () => {
    authService.logout();
    set({ user: null, isAuthenticated: false });
  },

  fetchProfile: async () => {
    if (!authService.isAuthenticated()) return;
    
    try {
      const user = await userService.getOwnProfile();
      set({ user, isAuthenticated: true });
    } catch (error) {
      console.error('Failed to fetch profile:', error);
      get().logout();
    }
  },

  updateUser: async (data: any) => {
    const updatedUser = await userService.updateOwnProfile(data);
    set({ user: updatedUser });
  },
}));
