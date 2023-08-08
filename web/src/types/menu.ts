import { ChipProps } from '@mui/material'
import { ReactElement, ReactNode } from 'react'
import { OverrideIcon } from '.'

export type MenuProps = {
  selectedItem: string[]
  drawerOpen: boolean
}

export type NavItemType = {
  id?: string
  icon?: OverrideIcon
  target?: boolean
  external?: string
  url?: string
  type?: string
  title?: ReactNode | ReactElement | JSX.Element | string
  color?: 'primary' | 'secondary' | 'default'
  caption?: ReactNode | ReactElement | JSX.Element | string
  breadcrumbs?: boolean
  disabled?: boolean
  chip?: ChipProps
  divider?: boolean
  children?: NavItemType[]
}

export type NavItemTypeObject = {
  children?: NavItemType[]
  items?: NavItemType[]
  type?: string
}
