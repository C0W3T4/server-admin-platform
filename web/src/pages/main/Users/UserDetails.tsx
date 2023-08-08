import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { UserTabDescription } from '../../../components/views/user/UserTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { userDetailsTabsOptions } from '../../../providers/userProvider'
import { TabsOptionsProps } from '../../../types/tabs'
import { UserProfile } from '../../../types/user'

const UserDetails = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<UserProfile>(`api/users/${id}`)

  const tabsPanel = [<UserTabDescription key={1} defaultValues={data} />]

  const updatedTabs = userDetailsTabsOptions.map(
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

export default UserDetails
