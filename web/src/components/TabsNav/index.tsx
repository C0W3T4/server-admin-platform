import { Tab, Tabs } from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { useState } from 'react'
import { FormattedMessage } from 'react-intl'
import { Link } from 'react-router-dom'
import { TabsNavProps } from '../../types/tabs'
import { TabPanel } from '../TabPanel'
import { MainCard } from '../cards/MainCard'

const a11yProps = (index: number) => {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  }
}

const TabsNav = ({ tabsOptions }: TabsNavProps) => {
  const theme = useTheme()
  const [value, setValue] = useState<number>(0)

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue)
  }

  return (
    <MainCard>
      <Tabs
        value={value}
        variant="scrollable"
        onChange={handleChange}
        textColor="secondary"
        indicatorColor="secondary"
        sx={{
          mb: 3,
          '& a': {
            minHeight: 'auto',
            minWidth: 10,
            py: 1.5,
            px: 1,
            mr: 2.2,
            color: theme.palette.grey[600],
            display: 'flex',
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'center',
          },
          '& a.Mui-selected': {
            color: theme.palette.primary.main,
          },
          '& a > svg': {
            mb: '0px !important',
            mr: 1.1,
          },
        }}
      >
        {tabsOptions.map((tab, index) => (
          <Tab
            key={index}
            component={Link}
            to="#"
            icon={tab.icon}
            label={<FormattedMessage id={tab.label} />}
            {...a11yProps(index)}
            sx={{ textTransform: 'none' }}
            disabled={tab.disabled}
          />
        ))}
      </Tabs>
      {tabsOptions.map((tab, index) => (
        <TabPanel key={index} index={index} value={value}>
          {tab.children}
        </TabPanel>
      ))}
    </MainCard>
  )
}

export default TabsNav
