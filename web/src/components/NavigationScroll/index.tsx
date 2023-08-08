import { ReactElement, useEffect } from 'react'
import { useLocation } from 'react-router-dom'

export const NavigationScroll = ({
  children,
}: {
  children: ReactElement | null
}) => {
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    })
  }, [pathname])

  return children || null
}
