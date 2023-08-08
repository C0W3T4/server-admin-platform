import { EditTwoTone } from '@mui/icons-material'
import { TabsOptionsProps } from '../types/tabs'

export const accountTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.myAccount',
    icon: <EditTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]
