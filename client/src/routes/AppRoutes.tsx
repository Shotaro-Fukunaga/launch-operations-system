import { Route, Routes } from "react-router-dom";
import { LaunchOperationPage } from "../page/LaunchOperationPage";

/**
 * アプリケーションのルートを定義するAppRoutesコンポーネント。
 *
 * @returns {JSX.Element} 定義されたルートを持つRoutesコンポーネント。
 */
export const AppRoutes: React.FC = (): JSX.Element => {
  return (
    <Routes>
      <Route path="/" element={<LaunchOperationPage />}></Route>
    </Routes>
  );
};
