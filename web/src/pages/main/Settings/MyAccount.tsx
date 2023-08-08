import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormMyAccount } from '../../../components/forms/user/FormMyAccount'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { accountTabsOptions } from '../../../providers/AccountProvider'
import { TabsOptionsProps } from '../../../types/tabs'
import { UserProfile } from '../../../types/user'

const MyAccount = () => {
  const { data, isLoading } = useAxiosGet<UserProfile>(`api/users/current`)

  const tabsPanel = [
    <FormMyAccount key={1} mode={'edit'} defaultValues={data} />,
  ]

  const updatedTabs = accountTabsOptions.map(
    (tab: TabsOptionsProps, index: number) => {
      return { ...tab, children: tabsPanel[index] }
    },
  )

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        {!isLoading && <TabsNav tabsOptions={updatedTabs} />}
      </Grid>
    </Grid>
  )
}

export default MyAccount
