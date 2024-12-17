import "./index.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext.tsx";
import GuestLayout from "./views/layouts/GuestLayout.tsx";
import App from "./views/App.tsx";
import AuthLayout from "./views/layouts/AuthLayout.tsx";
import LoginPage from "./views/login/LoginPage.tsx";
import RegisterPage from "./views/register/RegisterPage.tsx";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "./components/ui/sonner.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <AuthProvider>
          <Routes>
            <Route path="/" element={<GuestLayout />}>
              <Route path="/" element={<App />}></Route>
            </Route>
            <Route path="/auth" element={<AuthLayout />}>
              <Route path="login" element={<LoginPage />}></Route>
              <Route path="register" element={<RegisterPage />}></Route>
            </Route>
          </Routes>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
    <Toaster />
  </StrictMode>
);
