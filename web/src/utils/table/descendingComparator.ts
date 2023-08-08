import { KeyedObject } from '../../types'

export function descendingComparator(
  a: KeyedObject,
  b: KeyedObject,
  orderBy: string,
): 0 | 1 | -1 {
  if (b[orderBy] < a[orderBy]) {
    return -1
  }
  if (b[orderBy] > a[orderBy]) {
    return 1
  }
  return 0
}
