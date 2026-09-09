/// <reference types="vite/client" />
import { createClient } from '@supabase/supabase-js'

const metaEnv = (import.meta as any).env || {}
const supabaseUrl = metaEnv.VITE_SUPABASE_URL || 'https://jwyfmwffdwywkwiapbca.supabase.co'
const supabaseAnonKey = metaEnv.VITE_SUPABASE_ANON_KEY || 'sb_publishable_DlaiGU5vV0BKOQ5QXfSsCA_2yuFdcsB'


export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true,
  },
})
