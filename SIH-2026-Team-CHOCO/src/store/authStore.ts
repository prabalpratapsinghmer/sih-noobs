import { create } from 'zustand'
import { api } from '@/lib/api'
import { supabase } from '@/lib/supabase'

export interface UserProfile {
  user_id: string
  username: string
  email: string
  role: string
  station?: string
  badge_number?: string
  phone?: string
  avatar_url?: string
}

interface AuthState {
  user: UserProfile | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  isAuthModalOpen: boolean
  authModalMode: 'signin' | 'signup'
  authMessage: string | null
  redirectPath: string | null

  // Actions
  openAuthModal: (mode?: 'signin' | 'signup') => void
  openAuthModalWithPrompt: (message: string, redirect?: string) => void
  closeAuthModal: () => void
  setRedirectPath: (path: string | null) => void
  hasClearance: (allowedRoles: string[]) => boolean
  login: (usernameOrEmail: string, password: string) => Promise<{ success: boolean; error?: string }>
  signup: (data: {
    username: string
    email: string
    password: string
    full_name?: string
    role?: string
    station?: string
    badge_number?: string
    phone?: string
  }) => Promise<{ success: boolean; error?: string }>
  loginWithGoogle: (customPayload?: {
    email: string
    name: string
    avatar_url?: string
    google_id?: string
  }) => Promise<{ success: boolean; error?: string }>
  logout: () => Promise<void>
  checkSession: () => Promise<void>
}

const STORAGE_TOKEN_KEY = 'cybercell_auth_token'
const STORAGE_USER_KEY = 'cybercell_user'

export const useAuthStore = create<AuthState>((set, get) => ({
  user: (() => {
    try {
      const saved = localStorage.getItem(STORAGE_USER_KEY)
      return saved ? JSON.parse(saved) : null
    } catch {
      return null
    }
  })(),
  token: localStorage.getItem(STORAGE_TOKEN_KEY),
  isAuthenticated: !!localStorage.getItem(STORAGE_TOKEN_KEY),
  isLoading: false,
  error: null,
  isAuthModalOpen: false,
  authModalMode: 'signin',
  authMessage: null,
  redirectPath: null,

  openAuthModal: (mode = 'signin') => {
    set({ isAuthModalOpen: true, authModalMode: mode, error: null })
  },

  openAuthModalWithPrompt: (message: string, redirect?: string) => {
    set({
      isAuthModalOpen: true,
      authModalMode: 'signin',
      authMessage: message,
      redirectPath: redirect || null,
      error: null,
    })
  },

  closeAuthModal: () => {
    set({ isAuthModalOpen: false, error: null, authMessage: null })
  },

  setRedirectPath: (path: string | null) => {
    set({ redirectPath: path })
  },

  hasClearance: (allowedRoles: string[]) => {
    const user = get().user
    if (!user) return false
    const role = (user.role || '').toUpperCase()
    // Super Admin / Director has full clearance everywhere
    if (role === 'ADMIN' || user.username.toLowerCase() === 'moksh') return true
    return allowedRoles.map((r) => r.toUpperCase()).includes(role)
  },


  login: async (usernameOrEmail, password) => {
    set({ isLoading: true, error: null })
    try {
      const res = await api.auth.login({ username: usernameOrEmail, password })
      if (res.access_token && res.user) {
        localStorage.setItem(STORAGE_TOKEN_KEY, res.access_token)
        localStorage.setItem(STORAGE_USER_KEY, JSON.stringify(res.user))
        set({
          token: res.access_token,
          user: res.user,
          isAuthenticated: true,
          isLoading: false,
        })
        return { success: true }
      }
      throw new Error('Invalid response from authentication server')
    } catch (err: any) {
      const msg = err?.message || 'Login failed. Please verify credentials.'
      set({ error: msg, isLoading: false })
      return { success: false, error: msg }
    }
  },

  signup: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const res = await api.auth.signup(data)
      if (res.access_token && res.user) {
        localStorage.setItem(STORAGE_TOKEN_KEY, res.access_token)
        localStorage.setItem(STORAGE_USER_KEY, JSON.stringify(res.user))
        set({
          token: res.access_token,
          user: res.user,
          isAuthenticated: true,
          isLoading: false,
        })
        return { success: true }
      }
      throw new Error('Registration failed')
    } catch (err: any) {
      const msg = err?.message || 'Failed to create account. Username or email may already be registered.'
      set({ error: msg, isLoading: false })
      return { success: false, error: msg }
    }
  },

  loginWithGoogle: async (customPayload) => {
    set({ isLoading: true, error: null })
    try {
      if (customPayload) {
        // Direct / Sandbox Google Login
        const res = await api.auth.googleAuth(customPayload)
        if (res.access_token && res.user) {
          localStorage.setItem(STORAGE_TOKEN_KEY, res.access_token)
          localStorage.setItem(STORAGE_USER_KEY, JSON.stringify(res.user))
          set({
            token: res.access_token,
            user: res.user,
            isAuthenticated: true,
            isLoading: false,
          })
          return { success: true }
        }
      }

      // Supabase OAuth flow
      const { error: oauthError } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: window.location.origin,
        },
      })

      if (oauthError) {
        throw oauthError
      }

      return { success: true }
    } catch (err: any) {
      const msg = err?.message || 'Google authentication encountered an error.'
      set({ error: msg, isLoading: false })
      return { success: false, error: msg }
    }
  },

  logout: async () => {
    try {
      await api.auth.logout()
    } catch {
      // Ignore network errors on logout
    }
    try {
      await supabase.auth.signOut()
    } catch {
      // Ignore
    }
    localStorage.removeItem(STORAGE_TOKEN_KEY)
    localStorage.removeItem(STORAGE_USER_KEY)
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null,
    })
  },

  checkSession: async () => {
    // Check if returning from Supabase OAuth redirect
    try {
      const { data } = await supabase.auth.getSession()
      if (data?.session?.user) {
        const supaUser = data.session.user
        const res = await api.auth.googleAuth({
          email: supaUser.email || 'google.officer@cybercell.gov.in',
          name: supaUser.user_metadata?.full_name || supaUser.user_metadata?.name || 'Google Officer',
          avatar_url: supaUser.user_metadata?.avatar_url,
          google_id: supaUser.id,
        })
        if (res.access_token && res.user) {
          localStorage.setItem(STORAGE_TOKEN_KEY, res.access_token)
          localStorage.setItem(STORAGE_USER_KEY, JSON.stringify(res.user))
          set({
            token: res.access_token,
            user: res.user,
            isAuthenticated: true,
          })
          return
        }
      }
    } catch (e) {
      console.warn('OAuth session sync notice:', e)
    }

    // Check existing stored token
    const token = localStorage.getItem(STORAGE_TOKEN_KEY)
    if (token) {
      try {
        const me = await api.auth.getMe(token)
        if (me && me.user_id) {
          set({ user: me, isAuthenticated: true })
          localStorage.setItem(STORAGE_USER_KEY, JSON.stringify(me))
        }
      } catch {
        // Token invalid/expired
        // Keep user offline
      }
    }
  },
}))
