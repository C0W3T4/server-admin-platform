import { lazy } from 'react'
import { RouteObject } from 'react-router-dom'
import { Loadable } from '../components/Loadable'
import { MinimalLayout } from '../components/MinimalLayout'
import GuestGuard from '../guards/GuestGuard'

const AuthLogin = Loadable(lazy(() => import('../pages/authentication/Login')))
const AuthRegister = Loadable(
  lazy(() => import('../pages/authentication/Register')),
)

export const AuthRoutes: RouteObject = {
  path: '/',
  element: (
    <GuestGuard>
      <MinimalLayout />
    </GuestGuard>
  ),
  children: [
    {
      path: '',
      element: <AuthLogin />,
    },
    {
      path: 'register',
      element: <AuthRegister />,
    },
  ],
}
