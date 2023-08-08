import { EditTwoTone } from '@mui/icons-material'
import { TabsOptionsProps } from '../types/tabs'

export const settingSystemTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.system',
    icon: <EditTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]
