import { LinearProgressProps } from '@mui/material/LinearProgress'
import { LazyExoticComponent, Suspense } from 'react'
import { Loader } from '../Loader'

interface LoaderProps extends LinearProgressProps {}

export const Loadable =
  (Component: LazyExoticComponent<() => JSX.Element>) =>
  // eslint-disable-next-line react/display-name
  (props: LoaderProps) => (
    <Suspense fallback={<Loader />}>
      <Component {...props} />
    </Suspense>
  )
