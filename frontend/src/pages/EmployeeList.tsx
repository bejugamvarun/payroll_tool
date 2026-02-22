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
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Stack,
} from '@mui/material';
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Visibility as ViewIcon,
  Upload as UploadIcon,
} from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { employeesApi } from '../api/employees';
import { collegesApi } from '../api/colleges';
import { Employee, EmployeeCreate, College } from '../types';
import { useSnackbar } from '../context/SnackbarContext';

const EmployeeList: React.FC = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useSnackbar();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [colleges, setColleges] = useState<College[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
  const [filterCollege, setFilterCollege] = useState<number | ''>('');
  const [formData, setFormData] = useState<EmployeeCreate>({
    employee_code: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_joining: new Date().toISOString().split('T')[0],
    college_id: 0,
    department_id: 0,
    designation_id: 0,
    ctc: 0,
    monthly_gross: 0,
  });

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const collegeId = filterCollege === '' ? undefined : filterCollege;
      const data = await employeesApi.getAll(0, 100, collegeId);
      setEmployees(data);
    } catch (error) {
      showError('Failed to load employees');
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
    fetchEmployees();
  }, [filterCollege]);

  const handleOpenDialog = (employee?: Employee) => {
    if (employee) {
      setEditingEmployee(employee);
      setFormData({
        employee_code: employee.employee_code,
        first_name: employee.first_name,
        last_name: employee.last_name,
        email: employee.email,
        phone: employee.phone,
        date_of_joining: employee.date_of_joining,
        college_id: employee.college_id,
        department_id: employee.department_id,
        designation_id: employee.designation_id,
        ctc: employee.ctc,
        monthly_gross: employee.monthly_gross,
      });
    } else {
      setEditingEmployee(null);
      setFormData({
        employee_code: '',
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        date_of_joining: new Date().toISOString().split('T')[0],
        college_id: colleges.length > 0 ? colleges[0].id : 0,
        department_id: 0,
        designation_id: 0,
        ctc: 0,
        monthly_gross: 0,
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingEmployee(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingEmployee) {
        await employeesApi.update(editingEmployee.id, formData);
        showSuccess('Employee updated successfully');
      } else {
        await employeesApi.create(formData);
        showSuccess('Employee created successfully');
      }
      handleCloseDialog();
      fetchEmployees();
    } catch (error) {
      showError('Failed to save employee');
      console.error(error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this employee?')) {
      try {
        await employeesApi.delete(id);
        showSuccess('Employee deleted successfully');
        fetchEmployees();
      } catch (error) {
        showError('Failed to delete employee');
        console.error(error);
      }
    }
  };

  const columns: GridColDef[] = [
    { field: 'employee_code', headerName: 'Code', width: 120 },
    { field: 'first_name', headerName: 'First Name', flex: 1, minWidth: 150 },
    { field: 'last_name', headerName: 'Last Name', flex: 1, minWidth: 150 },
    { field: 'email', headerName: 'Email', flex: 1, minWidth: 200 },
    { field: 'phone', headerName: 'Phone', width: 150 },
    {
      field: 'is_active',
      headerName: 'Status',
      width: 100,
      renderCell: (params) => (params.value ? 'Active' : 'Inactive'),
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 120,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<ViewIcon />}
          label="View"
          onClick={() => navigate(`/employees/${params.id}`)}
        />,
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Edit"
          onClick={() => handleOpenDialog(params.row as Employee)}
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
        title="Employees"
        subtitle="Manage employee records"
        action={{
          label: 'Add Employee',
          onClick: () => handleOpenDialog(),
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
        <Button
          variant="outlined"
          startIcon={<UploadIcon />}
          onClick={() => navigate('/employees/bulk-upload')}
        >
          Bulk Upload
        </Button>
      </Stack>

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={employees}
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
        <DialogTitle>{editingEmployee ? 'Edit Employee' : 'Add Employee'}</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Employee Code"
              required
              value={formData.employee_code}
              onChange={(e) => setFormData({ ...formData, employee_code: e.target.value })}
              disabled={!!editingEmployee}
            />
            <TextField
              label="First Name"
              required
              value={formData.first_name}
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
            />
            <TextField
              label="Last Name"
              required
              value={formData.last_name}
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
            />
            <TextField
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
            <TextField
              label="Phone Number"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            />
            <TextField
              label="Date of Joining"
              type="date"
              required
              value={formData.date_of_joining}
              onChange={(e) => setFormData({ ...formData, date_of_joining: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
            <FormControl required>
              <InputLabel>College</InputLabel>
              <Select
                value={formData.college_id}
                label="College"
                onChange={(e) => setFormData({ ...formData, college_id: e.target.value as number })}
              >
                {colleges.map((college) => (
                  <MenuItem key={college.id} value={college.id}>
                    {college.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={!formData.employee_code || !formData.first_name || !formData.last_name}
          >
            {editingEmployee ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default EmployeeList;
