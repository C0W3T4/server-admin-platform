import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import useAuth from '../hooks/useAuth'
import { GuardProps } from '../types/guard'
import { UserType } from '../types/user'

interface RolesGuardProps extends GuardProps {
  user_type: UserType
  roles?: string[]
}

// eslint-disable-next-line camelcase
const RolesGuard = ({ children, user_type }: RolesGuardProps) => {
  const { user } = useAuth()
  const navigate = useNavigate()

  const userType: UserType[] = [
    UserType.NORMAL_USER,
    UserType.SYSTEM_AUDITOR,
    UserType.SYSTEM_ADMINISTRATOR,
    UserType.ADMIN,
  ]

  // eslint-disable-next-line camelcase
  const forbidden = (user_type: UserType, my_type: UserType): boolean => {
    return (
      // eslint-disable-next-line camelcase
      userType.findIndex((type) => type === my_type) <
      // eslint-disable-next-line camelcase
      userType.findIndex((type) => type === user_type)
    )
  }

  useEffect(() => {
    // eslint-disable-next-line camelcase
    if (user_type && user) {
      if (forbidden(user_type, user.user_type)) {
        navigate('/forbidden', { replace: true })
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [forbidden])

  // eslint-disable-next-line camelcase
  if (user_type && user) {
    if (!forbidden(user_type, user.user_type)) {
      return children
    } else {
      return null
    }
  } else {
    return children
  }
}

export default RolesGuard
