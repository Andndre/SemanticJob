import './index.css'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext.tsx'
import GuestLayout from './views/layouts/GuestLayout.tsx'
import App from './views/App.tsx'
import AuthLayout from './views/layouts/AuthLayout.tsx'
import LoginPage from './views/LoginPage.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
              <Route path="/" element={<GuestLayout/>}>
                <Route path="/" element={<App/>}></Route>
              </Route>
            <Route path="/auth" element={<AuthLayout/>}>
              <Route path="login" element={<LoginPage/>}></Route>
            </Route>
          </Routes>
        </AuthProvider>
      </BrowserRouter>
  </StrictMode>,
)
