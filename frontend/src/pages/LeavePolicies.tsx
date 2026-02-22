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
} from '@mui/material';
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { leavePoliciesApi } from '../api/leavePolicies';
import { collegesApi } from '../api/colleges';
import { LeavePolicy, LeavePolicyCreate, College } from '../types';
import { useSnackbar } from '../context/SnackbarContext';

const LeavePolicies: React.FC = () => {
  const { showSuccess, showError } = useSnackbar();
  const [policies, setPolicies] = useState<LeavePolicy[]>([]);
  const [colleges, setColleges] = useState<College[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingPolicy, setEditingPolicy] = useState<LeavePolicy | null>(null);
  const [formData, setFormData] = useState<LeavePolicyCreate>({
    name: '',
    college_id: 0,
    paid_leaves_per_year: 0,
    max_carry_forward: 0,
    comp_leave_enabled: false,
  });

  const fetchPolicies = async () => {
    try {
      setLoading(true);
      const data = await leavePoliciesApi.getAll();
      setPolicies(data);
    } catch (error) {
      showError('Failed to load leave policies');
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
    fetchPolicies();
  }, []);

  const handleOpenDialog = (policy?: LeavePolicy) => {
    if (policy) {
      setEditingPolicy(policy);
      setFormData({
        name: policy.name,
        college_id: policy.college_id,
        paid_leaves_per_year: policy.paid_leaves_per_year,
        max_carry_forward: policy.max_carry_forward,
        comp_leave_enabled: policy.comp_leave_enabled,
      });
    } else {
      setEditingPolicy(null);
      setFormData({
        name: '',
        college_id: colleges.length > 0 ? colleges[0].id : 0,
        paid_leaves_per_year: 0,
        max_carry_forward: 0,
        comp_leave_enabled: false,
      });
    }
    setDialogOpen(true);
  };

  const handleSubmit = async () => {
    try {
      if (editingPolicy) {
        await leavePoliciesApi.update(editingPolicy.id, formData);
        showSuccess('Leave policy updated successfully');
      } else {
        await leavePoliciesApi.create(formData);
        showSuccess('Leave policy created successfully');
      }
      setDialogOpen(false);
      fetchPolicies();
    } catch (error) {
      showError('Failed to save leave policy');
      console.error(error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this leave policy?')) {
      try {
        await leavePoliciesApi.delete(id);
        showSuccess('Leave policy deleted successfully');
        fetchPolicies();
      } catch (error) {
        showError('Failed to delete leave policy');
        console.error(error);
      }
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Policy Name', flex: 1, minWidth: 200 },
    { field: 'paid_leaves_per_year', headerName: 'Paid Leaves/Year', width: 150 },
    { field: 'max_carry_forward', headerName: 'Max Carry Forward', width: 150 },
    {
      field: 'comp_leave_enabled',
      headerName: 'Comp Leave',
      width: 130,
      renderCell: (params) => (params.value ? 'Enabled' : 'Disabled'),
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
          onClick={() => handleOpenDialog(params.row as LeavePolicy)}
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
        title="Leave Policies"
        subtitle="Manage leave allocations and policies"
        action={{
          label: 'Add Policy',
          onClick: () => handleOpenDialog(),
          icon: <AddIcon />,
        }}
      />

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={policies}
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
        <DialogTitle>{editingPolicy ? 'Edit Leave Policy' : 'Add Leave Policy'}</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Policy Name"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
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
            <TextField
              label="Paid Leaves Per Year"
              type="number"
              required
              value={formData.paid_leaves_per_year}
              onChange={(e) =>
                setFormData({ ...formData, paid_leaves_per_year: parseInt(e.target.value) || 0 })
              }
            />
            <TextField
              label="Max Carry Forward"
              type="number"
              value={formData.max_carry_forward}
              onChange={(e) =>
                setFormData({ ...formData, max_carry_forward: parseInt(e.target.value) || 0 })
              }
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={formData.comp_leave_enabled}
                  onChange={(e) => setFormData({ ...formData, comp_leave_enabled: e.target.checked })}
                />
              }
              label="Enable Compensatory Leaves"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" disabled={!formData.name}>
            {editingPolicy ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default LeavePolicies;
