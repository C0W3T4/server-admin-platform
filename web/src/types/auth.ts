import { UserProfile } from './user'

export interface JWTDataProps {
  userId: string
}

export type JWTContextType = {
  isLoggedIn: boolean
  isInitialized?: boolean
  user?: UserProfile | null | undefined
  logout: () => Promise<void>
  login: (email: string, password: string, company: string) => Promise<void>
}

export interface InitialLoginContextProps {
  isLoggedIn: boolean
  isInitialized?: boolean
  user?: UserProfile | null | undefined
}
