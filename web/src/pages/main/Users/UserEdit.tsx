import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormUser } from '../../../components/forms/user/FormUser'
import { UserOrganizationsList } from '../../../components/views/user/UserOrganizationsList'
import { UserTeamsList } from '../../../components/views/user/UserTeamsList'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { userEditTabsOptions } from '../../../providers/userProvider'
import { TabsOptionsProps } from '../../../types/tabs'
import { UserProfile } from '../../../types/user'

const UserEdit = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<UserProfile>(`api/users/${id}`)

  const tabsPanel = [
    <FormUser key={1} mode={'edit'} defaultValues={data} />,
    <UserOrganizationsList key={2} userData={data} />,
    <UserTeamsList key={3} userData={data} />,
  ]

  const updatedTabs = userEditTabsOptions.map(
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

export default UserEdit
