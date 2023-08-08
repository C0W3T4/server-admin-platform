import { Box } from '@mui/material'
import { TabsProps } from '../../types/tabs'

export function TabPanel({ children, value, index, ...rest }: TabsProps) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...rest}
    >
      {value === index && <Box>{children}</Box>}
    </div>
  )
}
