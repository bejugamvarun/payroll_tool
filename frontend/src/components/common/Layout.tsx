import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  School as SchoolIcon,
  People as PeopleIcon,
  AttachMoney as MoneyIcon,
  EventAvailable as LeaveIcon,
  Event as HolidayIcon,
  Assignment as AttendanceIcon,
  AccountBalance as PayrollIcon,
  Receipt as PayslipIcon,
  Assessment as ReportIcon,
} from '@mui/icons-material';

const drawerWidth = 260;

interface NavItem {
  label: string;
  path: string;
  icon: React.ReactElement;
}

interface NavSection {
  title: string;
  items: NavItem[];
}

const navSections: NavSection[] = [
  {
    title: 'OVERVIEW',
    items: [
      { label: 'Dashboard', path: '/', icon: <DashboardIcon /> },
    ],
  },
  {
    title: 'MANAGEMENT',
    items: [
      { label: 'Colleges', path: '/colleges', icon: <SchoolIcon /> },
      { label: 'Employees', path: '/employees', icon: <PeopleIcon /> },
      { label: 'Salary Components', path: '/salary-components', icon: <MoneyIcon /> },
    ],
  },
  {
    title: 'CONFIGURATION',
    items: [
      { label: 'Leave Policies', path: '/leave-policies', icon: <LeaveIcon /> },
      { label: 'Holidays', path: '/holidays', icon: <HolidayIcon /> },
    ],
  },
  {
    title: 'OPERATIONS',
    items: [
      { label: 'Attendance', path: '/attendance', icon: <AttendanceIcon /> },
      { label: 'Payroll', path: '/payroll', icon: <PayrollIcon /> },
    ],
  },
  {
    title: 'OUTPUTS',
    items: [
      { label: 'Payslips', path: '/payslips', icon: <PayslipIcon /> },
      { label: 'Reports', path: '/reports', icon: <ReportIcon /> },
    ],
  },
];

const Layout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: `calc(100% - ${drawerWidth}px)`,
          ml: `${drawerWidth}px`,
          bgcolor: 'primary.main',
        }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Payroll Management System
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="permanent"
        anchor="left"
      >
        <Toolbar sx={{ bgcolor: 'primary.dark' }}>
          <Typography variant="h6" sx={{ color: 'white', fontWeight: 600 }}>
            PAYROLL
          </Typography>
        </Toolbar>
        <Divider />

        {navSections.map((section) => (
          <Box key={section.title}>
            <ListItem>
              <Typography
                variant="caption"
                sx={{
                  fontWeight: 600,
                  color: 'text.secondary',
                  letterSpacing: 1.2,
                }}
              >
                {section.title}
              </Typography>
            </ListItem>
            <List disablePadding>
              {section.items.map((item) => (
                <ListItemButton
                  key={item.path}
                  selected={location.pathname === item.path}
                  onClick={() => navigate(item.path)}
                  sx={{
                    pl: 3,
                    '&.Mui-selected': {
                      bgcolor: 'primary.light',
                      color: 'primary.contrastText',
                      '& .MuiListItemIcon-root': {
                        color: 'primary.contrastText',
                      },
                      '&:hover': {
                        bgcolor: 'primary.light',
                      },
                    },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              ))}
            </List>
          </Box>
        ))}
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          bgcolor: 'background.default',
          p: 3,
          mt: 8,
          minHeight: '100vh',
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default Layout;
