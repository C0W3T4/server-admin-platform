import { LinearProgressProps } from '@mui/material/LinearProgress'
import { ComponentType, LazyExoticComponent, ReactNode, Suspense } from 'react'
import { Loader } from '../Loader'

interface LoaderProps extends LinearProgressProps {}

export const Loadable =
  (
    Component:
      | LazyExoticComponent<() => JSX.Element>
      | ComponentType<ReactNode>,
  ) =>
  (props: LoaderProps) => (
    <Suspense fallback={<Loader />}>
      <Component {...props} />
    </Suspense>
  )
