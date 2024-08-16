import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { LinearProgress } from '@mui/material';
import { useCallback, useEffect } from 'react';
import { useAppDispatch, useAppSelector } from './redux/hooks';
import { logOut, setUserAction } from './redux/user/slice';
import { getErrorSelector, getUserIsSet, getUserSelector } from './redux/user/selector';

function App() {
  const dispatch = useAppDispatch();

  const userIsSet = useAppSelector(getUserIsSet);
  const userError = useAppSelector(getErrorSelector);

  const currentUser = useAppSelector(getUserSelector);

  const logout = useCallback(() => {
    dispatch(logOut());
  }, [dispatch]);

  useEffect(() => {
    const user = getCurrentUser();
    if (user && !expiredToken()) {
      dispatch(setUserAction(user));
    } else {
      dispatch(logOut());
    }
  }, [dispatch, logout]);

  useEffect(() => {
    if (currentUser) {
      const expirationDate = new Date(currentUser.jwt.exp * 1000);
      const remainingTime = expirationDate.getTime() - new Date().getTime();
      logoutTimer = setTimeout(logout, remainingTime);
    } else {
      clearTimeout(logoutTimer);
    }
  }, [currentUser, dispatch, logout]);

  if (!userIsSet) {
    if (userError) {
      dispatch(logOut());
    }

    return <LinearProgress />;
  }
  
  return (
    <>
      
    </>
  )
}

export default App
