import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon, Visibility as ViewIcon } from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { collegesApi } from '../api/colleges';
import { College, CollegeCreate } from '../types';
import { useSnackbar } from '../context/SnackbarContext';

const CollegeList: React.FC = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useSnackbar();
  const [colleges, setColleges] = useState<College[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingCollege, setEditingCollege] = useState<College | null>(null);
  const [formData, setFormData] = useState<CollegeCreate>({
    serial_number: 0,
    college_code: '',
    name: '',
    address: '',
  });

  const fetchColleges = async () => {
    try {
      setLoading(true);
      const data = await collegesApi.getAll();
      setColleges(data);
    } catch (error) {
      showError('Failed to load colleges');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchColleges();
  }, []);

  const handleOpenDialog = (college?: College) => {
    if (college) {
      setEditingCollege(college);
      setFormData({
        serial_number: college.serial_number,
        college_code: college.college_code,
        name: college.name,
        address: college.address,
      });
    } else {
      setEditingCollege(null);
      setFormData({
        serial_number: 0,
        college_code: '',
        name: '',
        address: '',
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingCollege(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingCollege) {
        await collegesApi.update(editingCollege.id, formData);
        showSuccess('College updated successfully');
      } else {
        await collegesApi.create(formData);
        showSuccess('College created successfully');
      }
      handleCloseDialog();
      fetchColleges();
    } catch (error) {
      showError('Failed to save college');
      console.error(error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this college?')) {
      try {
        await collegesApi.delete(id);
        showSuccess('College deleted successfully');
        fetchColleges();
      } catch (error) {
        showError('Failed to delete college');
        console.error(error);
      }
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'serial_number', headerName: 'Serial No.', width: 100 },
    { field: 'college_code', headerName: 'Code', width: 120 },
    { field: 'name', headerName: 'College Name', flex: 1, minWidth: 200 },
    { field: 'address', headerName: 'Address', flex: 1, minWidth: 200 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 120,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<ViewIcon />}
          label="View"
          onClick={() => navigate(`/colleges/${params.id}`)}
        />,
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Edit"
          onClick={() => handleOpenDialog(params.row as College)}
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
        title="Colleges"
        subtitle="Manage college institutions"
        action={{
          label: 'Add College',
          onClick: () => handleOpenDialog(),
          icon: <AddIcon />,
        }}
      />

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={colleges}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50, 100]}
          initialState={{
            pagination: { paginationModel: { pageSize: 25 } },
          }}
          disableRowSelectionOnClick
        />
      </Box>

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>{editingCollege ? 'Edit College' : 'Add College'}</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Serial Number"
              type="number"
              required
              value={formData.serial_number}
              onChange={(e) => setFormData({ ...formData, serial_number: parseInt(e.target.value) || 0 })}
            />
            <TextField
              label="College Code"
              required
              value={formData.college_code}
              onChange={(e) => setFormData({ ...formData, college_code: e.target.value })}
            />
            <TextField
              label="College Name"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
            <TextField
              label="Address"
              multiline
              rows={2}
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" disabled={!formData.name || !formData.college_code}>
            {editingCollege ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CollegeList;
