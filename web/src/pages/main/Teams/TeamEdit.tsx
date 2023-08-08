import { Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import TabsNav from '../../../components/TabsNav'
import { FormTeam } from '../../../components/forms/team/FormTeam'
import { TeamUsersList } from '../../../components/views/team/TeamUsersList'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import { gridSpacing } from '../../../libs/redux/constants'
import { teamEditTabsOptions } from '../../../providers/TeamProvider'
import { TabsOptionsProps } from '../../../types/tabs'
import { TeamDataProps } from '../../../types/team'

const TeamEdit = () => {
  const { id } = useParams()

  const { data, isLoading } = useAxiosGet<TeamDataProps>(`api/teams/${id}`)

  const tabsPanel = [
    <FormTeam key={1} mode={'edit'} defaultValues={data} />,
    <TeamUsersList key={2} teamData={data} />,
  ]

  const updatedTabs = teamEditTabsOptions.map(
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

export default TeamEdit
