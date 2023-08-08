import {
  DateRangeTwoTone,
  Delete,
  EditTwoTone,
  Search,
  VisibilityTwoTone,
} from '@mui/icons-material'
import {
  Box,
  CardContent,
  Checkbox,
  Grid,
  IconButton,
  InputAdornment,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  TextField,
  Toolbar,
  Tooltip,
  Typography,
  Zoom,
  useTheme,
} from '@mui/material'
import { visuallyHidden } from '@mui/utils'
import React, { ChangeEvent, SyntheticEvent, useEffect, useState } from 'react'
import { TbCirclePlus } from 'react-icons/tb'
import { FormattedMessage, useIntl } from 'react-intl'
import { Link } from 'react-router-dom'
import { MainCard } from '../../../components/cards/MainCard'
import { useAxiosGet } from '../../../hooks/useAxiosGet'
import useConfig from '../../../hooks/useConfig'
import { useLoading } from '../../../hooks/useLoading'
import { api } from '../../../libs/axios'
import { dispatch } from '../../../libs/redux'
import { openSnackbar } from '../../../libs/redux/slices/snackbar'
import { organizationListTableHeadCells } from '../../../providers/OrganizationProvider'
import { ArrangementOrder, KeyedObject } from '../../../types'
import { OrganizationDataProps } from '../../../types/organization'
import { getComparator } from '../../../utils/table/getComparator'
import { stableSort } from '../../../utils/table/stableSort'

const iconSX = {
  width: 16,
  height: 16,
  verticalAlign: 'middle',
  mr: 0.5,
}

const OrganizationsList = () => {
  const theme = useTheme()
  const { formatMessage } = useIntl()
  const { locale } = useConfig()

  const { showLoading, hideLoading } = useLoading()
  const [order, setOrder] = useState<ArrangementOrder>('asc')
  const [orderBy, setOrderBy] = useState<string>('id')
  const [selected, setSelected] = useState<string[]>([])
  const [page, setPage] = useState<number>(0)
  const [rowsPerPage, setRowsPerPage] = useState<number>(5)
  const [search, setSearch] = useState<string>('')
  const [rows, setRows] = useState<OrganizationDataProps[]>([])

  const { data, setData } = useAxiosGet<OrganizationDataProps[]>(
    'api/assigns/users-organizations',
  )

  const handleSearch = (
    event?: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>,
  ) => {
    const newString = event?.target.value
    setSearch(newString || '')

    if (newString) {
      const newRows = rows.filter((row: KeyedObject) => {
        let matches = true

        const properties = ['id', 'name', 'created_at', 'created_by']
        let containsQuery = false

        properties.forEach((property) => {
          if (
            row[property]
              .toString()
              .toLowerCase()
              .includes(newString.toString().toLowerCase())
          ) {
            containsQuery = true
          }
        })

        if (!containsQuery) {
          matches = false
        }
        return matches
      })
      setRows(newRows)
    } else {
      setRows(data || [])
    }
  }

  const handleRequestSort = (
    _event: SyntheticEvent<Element, Event>,
    property: string,
  ) => {
    const isAsc = orderBy === property && order === 'asc'
    setOrder(isAsc ? 'desc' : 'asc')
    setOrderBy(property)
  }

  const handleSelectAllClick = (event?: ChangeEvent<HTMLInputElement>) => {
    if (event?.target.checked) {
      const newSelectedId = rows.map((row) => row.id)
      setSelected(newSelectedId)
      return
    }
    setSelected([])
  }

  const handleClick = (
    _event: React.MouseEvent<HTMLTableHeaderCellElement, MouseEvent>,
    name: string,
  ) => {
    const selectedIndex = selected.indexOf(name)
    let newSelected: string[] = []

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, name)
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1))
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1))
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1),
      )
    }

    setSelected(newSelected)
  }

  const handleChangePage = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent> | null,
    newPage: number,
  ) => {
    setPage(newPage)
  }

  const handleChangeRowsPerPage = (
    event: ChangeEvent<HTMLTextAreaElement | HTMLInputElement> | undefined,
  ) => {
    event?.target.value && setRowsPerPage(parseInt(event?.target.value, 10))
    setPage(0)
  }

  const isSelected = (name: string) => selected.indexOf(name) !== -1
  const emptyRows =
    page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0

  const deleteOrganization = async (selected: string[]) => {
    showLoading()
    await api
      .delete('api/organizations', { data: selected })
      .then((response) => {
        if (response.status === 204) {
          setData(
            data!.filter((organization) => !selected.includes(organization.id)),
          )
          dispatch(
            openSnackbar({
              open: true,
              message: <FormattedMessage id="snackbar.message.success.204" />,
              transition: 'SlideUp',
              variant: 'alert',
              alert: {
                color: 'success',
              },
              close: true,
            }),
          )
        }
      })
      .catch(() => {
        dispatch(
          openSnackbar({
            open: true,
            message: <FormattedMessage id="snackbar.message.error" />,
            transition: 'SlideUp',
            variant: 'alert',
            alert: {
              color: 'error',
            },
            close: true,
          }),
        )
      })
      .finally(() => hideLoading())
  }

  const handleDelete = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    selected: string[],
  ) => deleteOrganization(selected)

  useEffect(() => {
    setRows(data || [])
    handleSelectAllClick()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data])

  return (
    <MainCard
      title={<FormattedMessage id="organizations.list.title" />}
      content={false}
    >
      <CardContent>
        <Grid
          container
          justifyContent="space-between"
          alignItems="center"
          spacing={2}
        >
          <Grid item xs={12} sm={6}>
            <TextField
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search color="info" fontSize="small" />
                  </InputAdornment>
                ),
              }}
              onChange={handleSearch}
              placeholder={formatMessage({
                id: 'organizations.placeholders.searchOrganizations',
              })}
              value={search}
              size="small"
            />
          </Grid>
          <Grid item xs={12} sm={6} sx={{ textAlign: 'right' }}>
            <Tooltip
              TransitionComponent={Zoom}
              title={<FormattedMessage id="tooltips.create" />}
            >
              <Link to={'../create'}>
                <IconButton size="large" color="secondary">
                  <TbCirclePlus />
                </IconButton>
              </Link>
            </Tooltip>
          </Grid>
        </Grid>
      </CardContent>

      {/* table */}
      <TableContainer>
        <Table sx={{ minWidth: 750 }} aria-labelledby="tableTitle">
          {/* table header */}
          <TableHead>
            <TableRow>
              <TableCell padding="checkbox" sx={{ pl: 3 }}>
                <Checkbox
                  color="primary"
                  indeterminate={
                    selected.length > 0 && selected.length < rows.length
                  }
                  checked={rows.length > 0 && selected.length === rows.length}
                  onChange={handleSelectAllClick}
                  inputProps={{
                    'aria-label': 'select all desserts',
                  }}
                />
              </TableCell>
              {selected.length > 0 && (
                <TableCell padding="none" colSpan={8}>
                  {/* table toolbar */}
                  <Toolbar
                    sx={{
                      p: 0,
                      pl: 1,
                      pr: 1,
                      ...(selected.length > 0 && {
                        color: (theme) => theme.palette.secondary.main,
                      }),
                    }}
                  >
                    {selected.length > 0 && (
                      <Typography color="inherit" variant="h4">
                        {selected.length}{' '}
                        <FormattedMessage id="table.labels.selected" />
                      </Typography>
                    )}
                    <Box sx={{ flexGrow: 1 }} />
                    {selected.length > 0 && (
                      <Tooltip
                        TransitionComponent={Zoom}
                        title={<FormattedMessage id="tooltips.delete" />}
                      >
                        <IconButton
                          size="large"
                          onClick={(event) => handleDelete(event, selected)}
                        >
                          <Delete fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Toolbar>
                </TableCell>
              )}
              {selected.length <= 0 &&
                organizationListTableHeadCells.map((headCell) => (
                  <TableCell
                    key={headCell.id}
                    align={headCell.align}
                    padding={headCell.disablePadding ? 'none' : 'normal'}
                    sortDirection={orderBy === headCell.id ? order : false}
                  >
                    <TableSortLabel
                      active={orderBy === headCell.id}
                      direction={orderBy === headCell.id ? order : 'asc'}
                      onClick={(event) => handleRequestSort(event, headCell.id)}
                    >
                      <FormattedMessage id={headCell.label} />
                      {orderBy === headCell.id ? (
                        <Box component="span" sx={visuallyHidden}>
                          {order === 'desc'
                            ? 'sorted descending'
                            : 'sorted ascending'}
                        </Box>
                      ) : null}
                    </TableSortLabel>
                  </TableCell>
                ))}
              {selected.length <= 0 && (
                <TableCell sortDirection={false} align="center" sx={{ pr: 3 }}>
                  <Typography
                    variant="subtitle1"
                    sx={{
                      color:
                        theme.palette.mode === 'dark' ? 'grey.600' : 'grey.900',
                    }}
                  >
                    <FormattedMessage id="table.labels.actions" />
                  </Typography>
                </TableCell>
              )}
            </TableRow>
          </TableHead>

          {/* table body */}
          <TableBody>
            {stableSort<OrganizationDataProps>(
              rows,
              getComparator(order, orderBy),
            )
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row, index) => {
                /** Make sure no display bugs if row isn't an OrderData object */
                if (typeof row === 'number') return null

                const isItemSelected = isSelected(row.id)
                const labelId = `enhanced-table-checkbox-${index}`

                return (
                  <TableRow
                    hover
                    role="checkbox"
                    aria-checked={isItemSelected}
                    tabIndex={-1}
                    key={index}
                    selected={isItemSelected}
                  >
                    <TableCell
                      padding="checkbox"
                      sx={{ pl: 3 }}
                      onClick={(event) => handleClick(event, row.id)}
                    >
                      <Checkbox
                        color="primary"
                        checked={isItemSelected}
                        inputProps={{
                          'aria-labelledby': labelId,
                        }}
                      />
                    </TableCell>
                    <TableCell
                      component="th"
                      id={labelId}
                      scope="row"
                      onClick={(event) => handleClick(event, row.id)}
                      sx={{ cursor: 'pointer' }}
                    >
                      <Typography
                        variant="subtitle1"
                        sx={{
                          color:
                            theme.palette.mode === 'dark'
                              ? 'grey.600'
                              : 'grey.900',
                        }}
                      >
                        #{row.id}
                      </Typography>
                    </TableCell>
                    <TableCell align="left">{row.name}</TableCell>
                    <TableCell align="left">
                      <DateRangeTwoTone sx={iconSX} color="info" />
                      {new Intl.DateTimeFormat(locale, {
                        dateStyle: 'short',
                        timeStyle: 'medium',
                      }).format(new Date(row.created_at))}
                    </TableCell>
                    <TableCell align="left">{row.created_by}</TableCell>
                    <TableCell align="center" sx={{ pr: 3 }}>
                      <Tooltip
                        TransitionComponent={Zoom}
                        title={<FormattedMessage id="tooltips.viewDetails" />}
                      >
                        <Link to={`../details/${row.id}`}>
                          <IconButton color="secondary" size="large">
                            <VisibilityTwoTone sx={{ fontSize: '1.3rem' }} />
                          </IconButton>
                        </Link>
                      </Tooltip>
                      <Tooltip
                        TransitionComponent={Zoom}
                        title={<FormattedMessage id="tooltips.edit" />}
                      >
                        <Link to={`../edit/${row.id}`}>
                          <IconButton color="secondary" size="large">
                            <EditTwoTone sx={{ fontSize: '1.3rem' }} />
                          </IconButton>
                        </Link>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                )
              })}
            {(emptyRows > 0 || !data || data.length < 1) && (
              <TableRow hover>
                <TableCell colSpan={12} align="center">
                  <FormattedMessage id="errors.noData" />
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* table pagination */}
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={rows.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </MainCard>
  )
}

export default OrganizationsList
