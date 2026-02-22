import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  FormControlLabel,
  Checkbox,
  Stack,
} from '@mui/material';
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { holidaysApi } from '../api/holidays';
import { collegesApi } from '../api/colleges';
import { Holiday, HolidayCreate, College } from '../types';
import { useSnackbar } from '../context/SnackbarContext';
import { format } from 'date-fns';

const Holidays: React.FC = () => {
  const { showSuccess, showError } = useSnackbar();
  const [holidays, setHolidays] = useState<Holiday[]>([]);
  const [colleges, setColleges] = useState<College[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [filterCollege, setFilterCollege] = useState<number | ''>('');
  const [formData, setFormData] = useState<HolidayCreate>({
    name: '',
    date: new Date().toISOString().split('T')[0],
    college_id: 0,
    is_optional: false,
  });

  const fetchHolidays = async () => {
    try {
      setLoading(true);
      const collegeId = filterCollege === '' ? undefined : filterCollege;
      const data = await holidaysApi.getAll(collegeId, new Date().getFullYear());
      setHolidays(data);
    } catch (error) {
      showError('Failed to load holidays');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchColleges = async () => {
      try {
        const data = await collegesApi.getAll();
        setColleges(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchColleges();
  }, []);

  useEffect(() => {
    fetchHolidays();
  }, [filterCollege]);

  const handleOpenDialog = () => {
    setFormData({
      name: '',
      date: new Date().toISOString().split('T')[0],
      college_id: colleges.length > 0 ? colleges[0].id : 0,
      is_optional: false,
    });
    setDialogOpen(true);
  };

  const handleSubmit = async () => {
    try {
      await holidaysApi.create(formData);
      showSuccess('Holiday created successfully');
      setDialogOpen(false);
      fetchHolidays();
    } catch (error) {
      showError('Failed to create holiday');
      console.error(error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this holiday?')) {
      try {
        await holidaysApi.delete(id);
        showSuccess('Holiday deleted successfully');
        fetchHolidays();
      } catch (error) {
        showError('Failed to delete holiday');
        console.error(error);
      }
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Holiday Name', flex: 1, minWidth: 200 },
    {
      field: 'date',
      headerName: 'Date',
      width: 150,
      valueFormatter: (params) => format(new Date(params.value), 'dd MMM yyyy'),
    },
    {
      field: 'is_optional',
      headerName: 'Optional',
      width: 120,
      renderCell: (params) => (params.value ? 'Yes' : 'No'),
    },
    {
      field: 'college_id',
      headerName: 'Scope',
      width: 120,
      renderCell: (params) => (params.value ? 'College' : 'All'),
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 80,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Delete"
          onClick={() => handleDelete(params.id as number)}
        />,
      ],
    },
  ];

  return (
    <Box>
      <PageHeader
        title="Holidays"
        subtitle="Manage holiday calendar"
        action={{
          label: 'Add Holiday',
          onClick: handleOpenDialog,
          icon: <AddIcon />,
        }}
      />

      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Filter by College</InputLabel>
          <Select
            value={filterCollege}
            label="Filter by College"
            onChange={(e) => setFilterCollege(e.target.value as number | '')}
          >
            <MenuItem value="">All Colleges</MenuItem>
            {colleges.map((college) => (
              <MenuItem key={college.id} value={college.id}>
                {college.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Stack>

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={holidays}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: { paginationModel: { pageSize: 25 } },
          }}
          disableRowSelectionOnClick
        />
      </Box>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Holiday</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Holiday Name"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
            <TextField
              label="Date"
              type="date"
              required
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
            <FormControl required>
              <InputLabel>College</InputLabel>
              <Select
                value={formData.college_id}
                label="College"
                onChange={(e) =>
                  setFormData({ ...formData, college_id: e.target.value as number })
                }
              >
                {colleges.map((college) => (
                  <MenuItem key={college.id} value={college.id}>
                    {college.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControlLabel
              control={
                <Checkbox
                  checked={formData.is_optional}
                  onChange={(e) => setFormData({ ...formData, is_optional: e.target.checked })}
                />
              }
              label="Is Optional Holiday"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" disabled={!formData.name}>
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Holidays;
