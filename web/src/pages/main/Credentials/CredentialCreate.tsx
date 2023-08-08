import { Grid } from '@mui/material'
import TabsNav from '../../../components/TabsNav'
import { FormCredential } from '../../../components/forms/credential/FormCredential'
import { gridSpacing } from '../../../libs/redux/constants'
import { credentialCreateTabsOptions } from '../../../providers/CredentialProvider'
import { TabsOptionsProps } from '../../../types/tabs'

const CredentialCreate = () => {
  const tabsPanel = [<FormCredential key={1} mode={'create'} />]

  const updatedTabs = credentialCreateTabsOptions.map(
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

export default CredentialCreate
