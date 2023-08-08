import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { TeamTabDescription } from '../../../components/views/team/TeamTabDescription'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { teamDetailsTabsOptions } from '../../../providers/TeamProvider'
import { TabsOptionsProps } from '../../../types/tabs'
import { TeamDataProps } from '../../../types/team'

const TeamDetails = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<TeamDataProps>(`api/teams/${id}`)

  const tabsPanel = [<TeamTabDescription key={1} defaultValues={data} />]

  const updatedTabs = teamDetailsTabsOptions.map(
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

export default TeamDetails
