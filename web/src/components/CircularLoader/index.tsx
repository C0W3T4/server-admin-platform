import { CircularProgress } from '@mui/material'
import './styles.scss'

export const CircularLoader = () => (
  <div className="loading">
    <CircularProgress color="secondary" size={64} />
  </div>
)
