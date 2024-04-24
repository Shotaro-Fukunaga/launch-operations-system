import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import { BrowserRouter } from "react-router-dom";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  // KSP環境ローカルのみで動作させるため、React.StrictModeは使用しない
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
