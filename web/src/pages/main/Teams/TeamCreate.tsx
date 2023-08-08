import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormTeam } from '../../../components/forms/team/FormTeam'
import { gridSpacing } from '../../../libs/redux/constants'
import { teamCreateTabsOptions } from '../../../providers/TeamProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const TeamCreate = () => {
  const tabsPanel = [<FormTeam key={1} mode={'create'} />]

  const updatedTabs = teamCreateTabsOptions.map(
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

export default TeamCreate
