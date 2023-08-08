import { TableCellProps } from '@mui/material'
import { ChangeEvent, SyntheticEvent } from 'react'
import { ArrangementOrder } from '.'

export interface EnhancedTableHeadProps extends TableCellProps {
  onSelectAllClick: (e: ChangeEvent<HTMLInputElement>) => void
  order: ArrangementOrder
  orderBy?: string
  numSelected: number
  rowCount: number
  onRequestSort: (e: SyntheticEvent, p: string) => void
}

export type HeadCell = {
  id: string
  label: string
  numeric?: boolean
  disablePadding?: string | boolean | undefined
  align?: 'left' | 'right' | 'inherit' | 'center' | 'justify' | undefined
}
