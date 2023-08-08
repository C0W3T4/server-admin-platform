export function stableSort<T>(
  array: T[],
  comparator: (a: T, b: T) => number,
): (number | T)[] {
  const stabilizedThis = array.map((el: T, index: number) => [el, index])
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0] as T, b[0] as T)
    if (order !== 0) return order
    return (a[1] as number) - (b[1] as number)
  })
  return stabilizedThis.map((el) => el[0])
}
