import { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios'
import { useEffect, useState } from 'react'
import { useIntl } from 'react-intl'
import { useNavigate } from 'react-router-dom'
import { api } from '../libs/axios'
import { dispatch } from '../libs/redux'
import { openSnackbar } from '../libs/redux/slices/snackbar'

export const useAxiosGet = <T = unknown>(
  url: string,
  options?: AxiosRequestConfig,
) => {
  const navigate = useNavigate()
  const { formatMessage } = useIntl()

  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<AxiosError<T, unknown> | null>(null)

  const response = async () => {
    setIsLoading(true)

    await api
      .get(url, options)
      .then((response: AxiosResponse<T, unknown>) => setData(response.data))
      .catch((error: AxiosError<T, unknown>) => {
        setError(error)
        setTimeout(() => {
          if (error.response?.status === 401) {
            navigate('/unauthorized', { replace: true })
          }
          if (error.response?.status === 403) {
            navigate('/forbidden', { replace: true })
          }
          if (error.response?.status === 422) {
            navigate('/not-found', { replace: true })
          }
          if (error.response?.status === 404) {
            dispatch(
              openSnackbar({
                open: true,
                message: formatMessage({ id: 'snackbar.message.error.noData' }),
                transition: 'SlideUp',
                variant: 'alert',
                alert: {
                  color: 'error',
                },
                close: true,
              }),
            )
          }
        }, 1)
      })
      .finally(() => setIsLoading(false))
  }

  useEffect(() => {
    response()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return { data, setData, error, setError, isLoading }
}
