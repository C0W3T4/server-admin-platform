import { lazy } from 'react'
import { RouteObject } from 'react-router-dom'
import { Loadable } from '../components/Loadable'
import { MinimalLayout } from '../components/MinimalLayout'

const NotFound = Loadable(lazy(() => import('../pages/error/NotFound')))
const Unauthorized = Loadable(lazy(() => import('../pages/error/Unauthorized')))
const Forbidden = Loadable(lazy(() => import('../pages/error/Forbidden')))

export const ErrorRoutes: RouteObject = {
  path: '/',
  element: <MinimalLayout />,
  children: [
    {
      path: 'unauthorized',
      element: <Unauthorized />,
    },
    {
      path: 'forbidden',
      element: <Forbidden />,
    },
    {
      path: 'not-found',
      element: <NotFound />,
    },
    {
      path: '*',
      element: <NotFound />,
    },
  ],
}
