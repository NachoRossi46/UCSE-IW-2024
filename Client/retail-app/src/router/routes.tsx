import { DashboardLayout } from '../pages/layout/DashboardLayout';
import { DashboardPage } from '../pages/dashboard/DashboardPage';
import { createBrowserRouter } from "react-router-dom";
import { Root } from '../Root';
import { AuthLayout } from '../pages/layout/AuthLayout';
import InvoicesPage from '../pages/invoices/InvoicesPage';
import { LoginPage } from '../pages/login/LoginPage';

export const routes = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    children: [
      /// Dashboard Routes
      {
        path: "dashboard",
        element: <DashboardLayout />,
        children: [
          {
            path: '',
            element: <DashboardPage />
          },
          {
            path: 'invoices',
            element: <InvoicesPage />
          }
        ]
      },
      /// Auth Routes
      {
        
        path: 'auth',
        element: <AuthLayout />,
        children: [
          {
            path: 'login',
            element: <LoginPage />
          }
        ]
      },
    ],
  }
]);