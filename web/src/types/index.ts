import { SvgIconTypeMap } from '@mui/material'
import { OverridableComponent } from '@mui/material/OverridableComponent'
import {
  ChangeEvent,
  ComponentClass,
  Dispatch,
  FunctionComponent,
  ReactElement,
  ReactNode,
  SetStateAction,
} from 'react'
import { IconType } from 'react-icons'
import { MenuProps } from './menu'
import { SnackbarProps } from './snackbar'
import { UserStateProps } from './user'

export type ArrangementOrder = 'asc' | 'desc' | undefined

export type DateRange = { start: number | Date; end: number | Date }

export type KeyedObject = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: string | number | boolean | ReactElement | ReactNode | any
}

export type GetComparator = (
  o: ArrangementOrder,
  o1: string,
) => (a: KeyedObject, b: KeyedObject) => number

export type Direction = 'up' | 'down' | 'right' | 'left'

export type FormMode = 'create' | 'edit'

export type MapsProvidersProps = {
  label: string
  icon?: ReactElement | JSX.Element
}

export interface FormProps<T = null> {
  mode: FormMode
  defaultValues?: T | null
  setNewData?: Dispatch<SetStateAction<T | null>>
}

export interface DialogFormProps<T = null, Z = null> {
  open: boolean
  handleCloseDialog: () => void
  data?: T | null
  setNewData?: Dispatch<SetStateAction<Z | null>>
  oldData?: Z | null
}

export interface DetailsViewProps<T = null> {
  defaultValues: T | null
  setNewData?: Dispatch<SetStateAction<T | null>>
}

export type OverrideIcon =
  | (OverridableComponent<SvgIconTypeMap> & { muiName: string })
  | ComponentClass
  | FunctionComponent
  | IconType

export interface GenericCardProps {
  title?: string
  primary?: string | number | undefined
  secondary?: string
  content?: string
  image?: string
  dateTime?: string
  iconPrimary?: OverrideIcon
  color?: string
  size?: string
}

export type LinkTarget = '_blank' | '_self' | '_parent' | '_top'

export type AuthSliderProps = {
  title: string
  description: string
}

export interface DefaultRootStateProps {
  snackbar: SnackbarProps
  menu: MenuProps
  user: UserStateProps
}

export interface ColorPaletteProps {
  color: string
  label: string
  value: string
}

export interface ColorProps {
  readonly [key: string]: string
}

export type GuardProps = {
  children: ReactElement | null
}

export interface StringColorProps {
  id?: string
  label?: string
  color?: string
  primary?: string
  secondary?: string
}

export interface FormInputProps {
  bug: KeyedObject
  fullWidth?: boolean
  size?: 'small' | 'medium' | undefined
  label: string
  name: string
  required?: boolean
  InputProps?: {
    label: string
    startAdornment?: ReactNode
  }
}

export type StringBoolFunc = (s: string) => boolean
export type StringNumFunc = (s: string) => number
export type NumbColorFunc = (n: number) => StringColorProps | undefined
export type ChangeEventFunc = (e: ChangeEvent<HTMLInputElement>) => void
