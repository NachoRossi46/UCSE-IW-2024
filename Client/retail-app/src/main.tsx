import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
// import App from './App';
// import { Provider } from 'react-redux';
// // import { store } from './redux/store';
// // import { getMuiTheme } from './theme/theme';
// import { ThemeProvider as ThemeProviderLegacy } from '@mui/styles';
// import { StyledEngineProvider, ThemeProvider } from '@mui/material/styles';
// import { LocalizationProvider } from '@mui/x-date-pickers';
// import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
// import { QueryClient, QueryClientProvider } from 'react-query';
import { RouterProvider } from 'react-router-dom';

import './index.css';
import { routes } from './router/routes';

// const theme = getMuiTheme();
// const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={ routes } />
  </React.StrictMode>,
)

// const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
// root.render(
  // <ThemeProviderLegacy theme={theme}>
  //   <ThemeProvider theme={theme}>
      // <StyledEngineProvider injectFirst>
      //   {/* <Provider store={store}> */}
      //   <LocalizationProvider dateAdapter={AdapterDayjs}>
      //     <QueryClientProvider client={queryClient}>
      //       <App />
      //     </QueryClientProvider>
      //   </LocalizationProvider>
      //   {/* </Provider> */}
      // </StyledEngineProvider>
  //   </ThemeProvider>
  // </ThemeProviderLegacy>
// );
