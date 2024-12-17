import { createBrowserRouter } from "react-router-dom";
import App from "./views/App";
import GuestLayout from "./views/layouts/GuestLayout";
import AuthLayout from "./views/layouts/AuthLayout";
import LoginPage from "./views/LoginPage";

const Router = createBrowserRouter([
  {
    path: '/',
    element: <GuestLayout />,
    children: [
      {
        path: '/',
        element: <App />
      }
    ]
  },
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      {
        path: 'login',
        element: <LoginPage />
      }
    ]
  }
]);

export default Router;