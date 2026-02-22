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
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { salaryComponentsApi } from '../api/salaryComponents';
import { SalaryComponent, SalaryComponentCreate, ComponentType } from '../types';
import { useSnackbar } from '../context/SnackbarContext';

const SalaryComponents: React.FC = () => {
  const { showSuccess, showError } = useSnackbar();
  const [components, setComponents] = useState<SalaryComponent[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingComponent, setEditingComponent] = useState<SalaryComponent | null>(null);
  const [formData, setFormData] = useState<SalaryComponentCreate>({
    name: '',
    component_type: 'EARNING',
    description: '',
    is_default: false,
  });

  const fetchComponents = async () => {
    try {
      setLoading(true);
      const data = await salaryComponentsApi.getAll();
      setComponents(data);
    } catch (error) {
      showError('Failed to load salary components');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComponents();
  }, []);

  const handleOpenDialog = (component?: SalaryComponent) => {
    if (component) {
      setEditingComponent(component);
      setFormData({
        name: component.name,
        component_type: component.component_type,
        description: component.description,
        is_default: component.is_default,
      });
    } else {
      setEditingComponent(null);
      setFormData({
        name: '',
        component_type: 'EARNING',
        description: '',
        is_default: false,
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingComponent(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingComponent) {
        await salaryComponentsApi.update(editingComponent.id, formData);
        showSuccess('Salary component updated successfully');
      } else {
        await salaryComponentsApi.create(formData);
        showSuccess('Salary component created successfully');
      }
      handleCloseDialog();
      fetchComponents();
    } catch (error) {
      showError('Failed to save salary component');
      console.error(error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this salary component?')) {
      try {
        await salaryComponentsApi.delete(id);
        showSuccess('Salary component deleted successfully');
        fetchComponents();
      } catch (error) {
        showError('Failed to delete salary component');
        console.error(error);
      }
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Component Name', flex: 1, minWidth: 200 },
    {
      field: 'component_type',
      headerName: 'Type',
      width: 120,
      renderCell: (params) => (
        <Box
          sx={{
            color: params.value === 'EARNING' ? 'success.main' : 'error.main',
            fontWeight: 600,
          }}
        >
          {params.value}
        </Box>
      ),
    },
    { field: 'description', headerName: 'Description', flex: 1, minWidth: 200 },
    {
      field: 'is_default',
      headerName: 'Default',
      width: 100,
      renderCell: (params) => (params.value ? 'Yes' : 'No'),
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 100,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Edit"
          onClick={() => handleOpenDialog(params.row as SalaryComponent)}
        />,
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
        title="Salary Components"
        subtitle="Manage earnings and deductions"
        action={{
          label: 'Add Component',
          onClick: () => handleOpenDialog(),
          icon: <AddIcon />,
        }}
      />

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={components}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: { paginationModel: { pageSize: 25 } },
          }}
          disableRowSelectionOnClick
        />
      </Box>

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingComponent ? 'Edit Salary Component' : 'Add Salary Component'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Component Name"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
            <TextField
              select
              label="Component Type"
              required
              value={formData.component_type}
              onChange={(e) =>
                setFormData({ ...formData, component_type: e.target.value as ComponentType })
              }
            >
              <MenuItem value="EARNING">Earning</MenuItem>
              <MenuItem value="DEDUCTION">Deduction</MenuItem>
            </TextField>
            <TextField
              label="Description"
              multiline
              rows={2}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={formData.is_default}
                  onChange={(e) => setFormData({ ...formData, is_default: e.target.checked })}
                />
              }
              label="Is Default Component"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" disabled={!formData.name}>
            {editingComponent ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SalaryComponents;
