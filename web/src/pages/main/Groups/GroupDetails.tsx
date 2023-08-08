import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { GroupTabDescription } from '../../../components/views/group/GroupTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { groupDetailsTabsOptions } from '../../../providers/GroupProvider'
import { GroupDataProps } from '../../../types/group'
import { TabsOptionsProps } from '../../../types/tabs'

const GroupDetails = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<GroupDataProps>(`api/groups/${id}`)

  const tabsPanel = [<GroupTabDescription key={1} defaultValues={data} />]

  const updatedTabs = groupDetailsTabsOptions.map(
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

export default GroupDetails
