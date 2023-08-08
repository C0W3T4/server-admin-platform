import { InputLabelProps, InputLabel as MuiInputLabel } from '@mui/material'
import { experimentalStyled as styled } from '@mui/material/styles'

interface MUIInputLabelProps extends InputLabelProps {
  horizontal?: boolean
}

const BInputLabel = styled(
  (props: MUIInputLabelProps) => <MuiInputLabel {...props} />,
  {
    shouldForwardProp: (prop) => prop !== 'horizontal',
  },
)(({ theme, horizontal }) => ({
  color: theme.palette.text.primary,
  fontWeight: 500,
  marginBottom: horizontal ? 0 : 8,
}))

const InputLabel = ({
  children,
  horizontal,
  ...others
}: MUIInputLabelProps) => (
  <BInputLabel horizontal={horizontal} {...others}>
    {children}
  </BInputLabel>
)

InputLabel.defaultProps = {
  horizontal: false,
}

export default InputLabel
