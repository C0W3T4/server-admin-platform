import { ReactNode, createContext, useState } from 'react'
import { CircularLoader } from '../components/CircularLoader'

export type LoadingContextType = {
  loading: boolean
  showLoading: () => void
  hideLoading: () => void
}

export const LoadingContext = createContext<LoadingContextType | null>(null)

export const LoadingProvider = ({ children }: { children: ReactNode }) => {
  const [loading, setLoading] = useState<boolean>(false)

  return (
    <LoadingContext.Provider
      value={{
        loading,
        showLoading: () => setLoading(true),
        hideLoading: () => setLoading(false),
      }}
    >
      <>
        {loading && <CircularLoader />}
        {children}
      </>
    </LoadingContext.Provider>
  )
}
