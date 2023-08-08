import { ReactElement, ReactNode } from 'react'

export interface TabsProps {
  children?: ReactElement | ReactNode | string
  value: string | number
  index: number
}

export interface TabsOptionsProps {
  label: string
  children?: ReactElement | ReactNode | JSX.Element | string
  icon?: ReactElement | JSX.Element
  disabled?: boolean
}

export interface TabsNavProps {
  tabsOptions: TabsOptionsProps[]
  children?: ReactElement | ReactNode | JSX.Element | string
}
