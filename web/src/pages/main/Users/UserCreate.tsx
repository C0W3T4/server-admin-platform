import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormUser } from '../../../components/forms/user/FormUser'
import { gridSpacing } from '../../../libs/redux/constants'
import { userCreateTabsOptions } from '../../../providers/userProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const UserCreate = () => {
  const tabsPanel = [<FormUser key={1} mode={'create'} />]

  const updatedTabs = userCreateTabsOptions.map(
    (tab: TabsOptionsProps, index: number) => {
      return { ...tab, children: tabsPanel[index] }
    },
  )

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        <TabsNav tabsOptions={updatedTabs} />
      </Grid>
    </Grid>
  )
}

export default UserCreate
