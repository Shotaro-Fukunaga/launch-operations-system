import { Route, Routes } from "react-router-dom";
import { LaunchDataViewer } from "../feature/launch-view/page/LaunchDataViewer";

/**
 * アプリケーションのルートを定義するAppRoutesコンポーネント。
 *
 * @returns {JSX.Element} 定義されたルートを持つRoutesコンポーネント。
 */
export const AppRoutes: React.FC = (): JSX.Element => {
  return (
    <Routes>
      <Route path="/" element={<LaunchDataViewer />}></Route>
    </Routes>
  );
};
