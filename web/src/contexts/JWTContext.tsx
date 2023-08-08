import jwtDecode from 'jwt-decode'
import { ReactElement, createContext, useEffect, useReducer } from 'react'
import { Loader } from '../components/Loader'
import { api } from '../libs/axios'
import accountReducer from '../libs/redux/accountReducer'
import { LOGIN, LOGOUT } from '../libs/redux/actions'
import { KeyedObject } from '../types'
import { InitialLoginContextProps, JWTContextType } from '../types/auth'
import { LoginResponseProps, UserProfile } from '../types/user'

const initialState: InitialLoginContextProps = {
  isLoggedIn: false,
  isInitialized: false,
  user: null,
}

const verifyToken: (st: string) => boolean = (serviceToken) => {
  if (!serviceToken) {
    return false
  }
  const decoded: KeyedObject = jwtDecode(serviceToken)

  if (decoded.exp) {
    return decoded.exp > Date.now() / 1000
  } else {
    return true
  }
}

const setSession = (serviceToken?: string | null) => {
  if (serviceToken) {
    localStorage.setItem('serviceToken', serviceToken)
    api.defaults.headers.common.Authorization = `Bearer ${serviceToken}`
  } else {
    localStorage.removeItem('serviceToken')
    delete api.defaults.headers.common.Authorization
  }
}

const JWTContext = createContext<JWTContextType | null>(null)

export const JWTProvider = ({ children }: { children: ReactElement }) => {
  const [state, dispatch] = useReducer(accountReducer, initialState)

  useEffect(() => {
    const init = async () => {
      try {
        const serviceToken = window.localStorage.getItem('serviceToken')

        if (serviceToken && verifyToken(serviceToken)) {
          setSession(serviceToken)
          const response = await api.get('/api/users/current')
          const user: UserProfile = response.data

          dispatch({
            type: LOGIN,
            payload: {
              isLoggedIn: true,
              user,
            },
          })
        } else {
          dispatch({
            type: LOGOUT,
          })
        }
      } catch (err) {
        dispatch({
          type: LOGOUT,
        })
      }
    }

    init()
  }, [])

  const login = async (
    username: string,
    password: string,
    // eslint-disable-next-line camelcase
    client_id: string,
  ) => {
    const response = await api.request({
      method: 'POST',
      url: '/api/login',
      // eslint-disable-next-line camelcase
      data: { username, password, client_id },
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    // eslint-disable-next-line camelcase
    const { access_token, user }: LoginResponseProps = response.data

    setSession(access_token)
    dispatch({
      type: LOGIN,
      payload: {
        isLoggedIn: true,
        user,
      },
    })
  }

  const logout = async () => {
    setSession(null)
    dispatch({ type: LOGOUT })
  }

  if (state.isInitialized !== undefined && !state.isInitialized) {
    return <Loader />
  }

  return (
    <JWTContext.Provider value={{ ...state, login, logout }}>
      {children}
    </JWTContext.Provider>
  )
}

export default JWTContext
