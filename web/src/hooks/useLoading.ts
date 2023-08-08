import { useContext } from 'react'
import { LoadingContext } from '../contexts/LoadingContext'

export const useLoading = () => {
  const context = useContext(LoadingContext)

  if (!context) throw new Error('context must be use inside provider')

  return context
}
