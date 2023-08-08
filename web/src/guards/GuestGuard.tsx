import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { DASHBOARD_PATH } from '../configs/defaultConfig'
import useAuth from '../hooks/useAuth'
import { GuardProps } from '../types/guard'

const GuestGuard = ({ children }: GuardProps) => {
  const { isLoggedIn } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (isLoggedIn) {
      navigate(DASHBOARD_PATH, { replace: true })
    }
  }, [isLoggedIn, navigate])

  return children
}

export default GuestGuard
