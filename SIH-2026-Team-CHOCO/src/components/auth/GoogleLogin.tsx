import React, { useEffect, useRef } from 'react'
import { useAuthStore } from '@/store/authStore'
import { useNavigate } from 'react-router-dom'

interface GoogleLoginProps {
  onSuccess?: () => void
}

export const GoogleLogin: React.FC<GoogleLoginProps> = ({ onSuccess }) => {
  const buttonRef = useRef<HTMLDivElement>(null)
  const { loginWithGoogle, closeAuthModal, setRedirectPath, redirectPath } = useAuthStore()
  const navigate = useNavigate()

  useEffect(() => {
    // Load Google Identity Services script
    const script = document.createElement('script')
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true
    document.body.appendChild(script)

    script.onload = () => {
      if (window.google) {
        const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
        if (!clientId) {
          console.warn('[GAURDIAN] Google OAuth client ID not configured. Set VITE_GOOGLE_CLIENT_ID in .env');
          return;
        }
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: async (response: GoogleCredentialResponse) => {
            if (response.credential) {
              const res = await loginWithGoogle({
                credential: response.credential,
                google_id: response.credential,
              })
              if (res.success) {
                if (onSuccess) onSuccess()
                closeAuthModal()
                if (redirectPath) {
                  navigate(redirectPath)
                  setRedirectPath(null)
                }
              }
            }
          },
        })

        if (buttonRef.current) {
          window.google.accounts.id.renderButton(buttonRef.current, {
            theme: 'outline',
            size: 'large',
            width: 320,
            shape: 'rectangular',
          })
        }
      }
    }

    return () => {
      document.body.removeChild(script)
    }
  }, [loginWithGoogle, onSuccess, closeAuthModal, navigate, redirectPath, setRedirectPath])

  return (
    <div className="flex justify-center w-full">
      <div ref={buttonRef}></div>
    </div>
  )
}
