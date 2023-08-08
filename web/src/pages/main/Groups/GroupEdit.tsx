import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormGroup } from '../../../components/forms/group/FormGroup'
import { GroupHostsList } from '../../../components/views/group/GroupHostsList'
import { GroupTeamsList } from '../../../components/views/group/GroupTeamsList'
import { GroupUsersList } from '../../../components/views/group/GroupUsersList'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { groupEditTabsOptions } from '../../../providers/GroupProvider'
import { GroupDataProps } from '../../../types/group'
import { TabsOptionsProps } from '../../../types/tabs'

const GroupEdit = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<GroupDataProps>(`api/groups/${id}`)

  const tabsPanel = [
    <FormGroup key={1} mode={'edit'} defaultValues={data} />,
    <GroupUsersList key={2} groupData={data} />,
    <GroupTeamsList key={3} groupData={data} />,
    <GroupHostsList key={4} groupData={data} />,
  ]

  const updatedTabs = groupEditTabsOptions.map(
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

export default GroupEdit
