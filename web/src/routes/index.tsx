import { useRoutes } from 'react-router-dom'
import { AuthRoutes } from './AuthRoutes'
import { ErrorRoutes } from './ErrorRoutes'
import { MainRoutes } from './MainRoutes'

export const AppRoutes = () => useRoutes([AuthRoutes, MainRoutes, ErrorRoutes])
