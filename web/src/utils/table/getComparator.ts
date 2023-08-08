import { ArrangementOrder, GetComparator, KeyedObject } from '../../types'
import { descendingComparator } from './descendingComparator'

export const getComparator: GetComparator = (
  order: ArrangementOrder,
  orderBy: string,
) =>
  order === 'desc'
    ? (a: KeyedObject, b: KeyedObject) => descendingComparator(a, b, orderBy)
    : (a: KeyedObject, b: KeyedObject) => -descendingComparator(a, b, orderBy)
