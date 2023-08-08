import { ReactNode, useEffect, useState } from 'react'
import { IntlProvider, MessageFormatElement } from 'react-intl'
import useConfig from '../../hooks/useConfig'

const loadLocaleData = (locale: string) => {
  switch (locale) {
    case 'pt':
      return import('../../assets/locales/pt_pt.json')
    default:
      return import('../../assets/locales/en_uk.json')
  }
}

interface LocalsProps {
  children: ReactNode
}

const Locales = ({ children }: LocalsProps) => {
  const { locale } = useConfig()
  const [messages, setMessages] = useState<
    Record<string, string> | Record<string, MessageFormatElement[]> | undefined
  >()

  useEffect(() => {
    loadLocaleData(locale).then(
      (d: {
        default:
          | Record<string, string>
          | Record<string, MessageFormatElement[]>
          | undefined
      }) => {
        setMessages(d.default)
      },
    )
  }, [locale])

  return (
    <>
      {messages && (
        <IntlProvider locale={locale} defaultLocale="en" messages={messages}>
          {children}
        </IntlProvider>
      )}
    </>
  )
}

export default Locales
