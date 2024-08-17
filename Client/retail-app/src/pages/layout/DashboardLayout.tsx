import SideMenu from '../../components/dashboard/sidenav';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../../store/auth/auth.store';

export const DashboardLayout = () => {

  const authStatus = useAuthStore( state => state.status );
  const checkAuthStatus = useAuthStore( state => state.checkAuthStatus );

  if ( authStatus === 'Pending' ) {
    checkAuthStatus();
    return <div>Loading...</div> //TODO Create a skeleton for the dashboard here
  }

  if (authStatus === 'Unauthorized')
    return <Navigate to="/auth/login" />

  return (
    <div className="bg-slate-200 overflow-y-scroll w-screen h-screen antialiased text-slate-900 selection:bg-blue-900 selection:text-white">
      <div className="flex flex-row relative w-screen">
        <SideMenu />

        <div className="w-full p-4">
          <Outlet />
        </div>

      </div>

    </div>
  );
};