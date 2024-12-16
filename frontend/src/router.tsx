import {createBrowserRouter, Navigate} from "react-router-dom";
import App from "./views/App";
import GuestLayout from "./views/layouts/GuestLayout";

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
	}
]);

export default Router;
